#!/usr/bin/env bash
set -euo pipefail
set -a; source "${@PREFIX@_GPU_CONFIG:-$HOME/.config/@SITE@-gpu/gpu.env}"; set +a
: "${SLURM_JOB_ID:?allocation required}"
job_id="$SLURM_JOB_ID"; host_name="$(hostname -s)"; socket="gpu-$job_id"; session=work
core_bin="${HPC_CORE_BIN:-$HOME/.local/bin}"
state_dir="${@PREFIX@_GPU_STATE_DIR:-$HOME/.local/state/@SITE@-gpu}"
route_dir="$state_dir/routes"; route_file="$route_dir/$job_id.route"
expand_path() { python3 -c 'import os,sys; p=os.path.expandvars(sys.argv[1]); assert "$" not in p and os.path.isabs(p), "unresolved or relative path"; print(p)' "$1"; }
local_base="$(expand_path "$HPC_LOCAL_TEMPLATE")"
export @PREFIX@_LOCAL_BASE="$local_base" @PREFIX@_WORKSPACE="$local_base/workspace"
export HPC_ALLOWED_LOCAL_PREFIX="$(expand_path "$HPC_LOCAL_PREFIX")"
export @PREFIX@_LOCAL_SNAPSHOT_ARCHIVE="$(expand_path "$HPC_ARCHIVE")"
export UV_CACHE_DIR="$local_base/cache/uv" UV_LINK_MODE=hardlink
export @PREFIX@_GPU_STATE_DIR="$state_dir"
inner_tmux=(tmux -L "$socket" -f "$HOME/.config/@SITE@-gpu/tmux.compute.conf")
@BOOT_GUARD@
unset TMUX TMUX_PANE TMOUT
mkdir -p "$route_dir" "$local_base/workspace" "$UV_CACHE_DIR" "$HOME/logs/@SITE@"
"$core_bin/@SITE@-allocation" bind "$HPC_ALLOCATION_REQUEST_ID" --job "$job_id"
"$core_bin/@SITE@-local-snapshot" restore > "$HOME/logs/@SITE@/restore-$job_id.log" 2>&1
"${inner_tmux[@]}" new-session -d -s work -n setup -c "$local_base/workspace" /bin/bash --noprofile --norc
for key in SLURM_JOB_ID HPC_CORE_BIN HPC_ALLOWED_LOCAL_PREFIX @PREFIX@_LOCAL_BASE @PREFIX@_WORKSPACE @PREFIX@_LOCAL_SNAPSHOT_ARCHIVE @PREFIX@_GPU_AUTOSAVE_INTERVAL UV_CACHE_DIR UV_LINK_MODE; do
  [[ -z "${!key:-}" ]] || "${inner_tmux[@]}" set-environment -g "$key" "${!key}"
done
end_time="$(scontrol show job "$job_id" -o | sed -n 's/.* EndTime=\([^ ]*\).*/\1/p')"
end_epoch="$(date -d "$end_time" +%s 2>/dev/null || true)"
[[ -z "$end_epoch" ]] || "${inner_tmux[@]}" set-environment -g HPC_SNAPSHOT_END_EPOCH "$end_epoch"
# Site/repository toolchain setup belongs in an explicitly configured hook.
if [[ -n "${HPC_BOOT_HOOK:-}" ]]; then "$HPC_BOOT_HOOK"; fi
printf -v autosave '%q ' "$core_bin/@SITE@-local-snapshot" autosave "${@PREFIX@_GPU_AUTOSAVE_INTERVAL:-300}"
"${inner_tmux[@]}" new-window -d -t work: -n autosave /bin/bash --noprofile --norc
printf -v log '%q' "$HOME/logs/@SITE@/autosave-$job_id.log"
"${inner_tmux[@]}" send-keys -t work:autosave -l "exec ${autosave% } >> $log 2>&1"
"${inner_tmux[@]}" send-keys -t work:autosave Enter
"$core_bin/@SITE@-local-snapshot" ready
printf '%s\t%s\t%s\t%s\n' "$job_id" "$host_name" "$socket" work > "$route_file.tmp.$$"
mv -f "$route_file.tmp.$$" "$route_file"
"$core_bin/@SITE@-allocation" bind "$HPC_ALLOCATION_REQUEST_ID" --job "$job_id" --ready
trap 'rm -f "$route_file"' EXIT
flock -u 8; exec 8>&-
"${inner_tmux[@]}" attach -t work || true
while "${inner_tmux[@]}" has-session -t work 2>/dev/null; do sleep 60; done
