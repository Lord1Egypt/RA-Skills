#!/usr/bin/env bash
set -euo pipefail
config_file="${PSC_GPU_CONFIG:-$HOME/.config/psc-gpu/gpu.env}"
if [[ -r "$config_file" ]]; then set -a; source "$config_file"; set +a; fi

outer_socket="${PSC_GPU_OUTER_SOCKET:-}"
outer_target="${PSC_GPU_OUTER_TARGET:-}"
outer_pane_pid="${PSC_GPU_OUTER_PANE_PID:-}"
unset TMOUT
unset PSC_GPU_OUTER_SOCKET PSC_GPU_OUTER_TARGET PSC_GPU_OUTER_PANE_PID
unset TMUX TMUX_PANE
export TERM=xterm-256color

: "${SLURM_JOB_ID:?psc-gpu-boot must run inside a Slurm allocation}"
# Some PSC GPU nodes expose /local itself as the allocation's scratch root.
# Keep the workspace below that root so restore never operates on /local.
if [[ ( "${LOCAL:-}" == /local || -z "${LOCAL:-}" ) &&
      ! -w "/local/slurm-${SLURM_JOB_ID}/local" && -w /local ]]; then
    export LOCAL="/local/$USER/hpc-job-$SLURM_JOB_ID"
    mkdir -p "$LOCAL"
fi

if [[ -f "$HOME/.psc-local-env.sh" ]]; then
    # Refresh LOCAL and cache paths after Slurm places the shell on the node.
    source "$HOME/.psc-local-env.sh"
fi

toolchain_config="${PSC_GPU_TOOLCHAIN_CONFIG:-$HOME/.config/psc-gpu/toolchain.env}"
if [[ "${PSC_TOOLCHAIN_DISABLED:-0}" == 1 ]]; then
    echo 'psc-gpu-boot: site-wide toolchain setup disabled; use repository launchers'
elif [[ -r "$toolchain_config" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$toolchain_config"
    set +a
    if ! type module >/dev/null 2>&1; then
        for module_init in /etc/profile.d/modules.sh /usr/share/lmod/lmod/init/bash; do
            if [[ -r "$module_init" ]]; then
                # shellcheck disable=SC1090
                source "$module_init"
                break
            fi
        done
    fi
    type module >/dev/null 2>&1 || {
        printf 'psc-gpu-boot: PSC module command is unavailable\n' >&2
        exit 2
    }
    module load "$GCC_MODULE"
    export CC CXX CUDA_HOME
    export PSC_GPU_TOOLCHAIN_READY=1
    export PATH="$CUDA_HOME/bin:$PATH"
    export LD_LIBRARY_PATH="$CUDA_HOME/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
else
    printf 'psc-gpu-boot: missing toolchain config: %s\n' "$toolchain_config" >&2
    exit 2
fi

: "${SLURM_JOB_ID:?psc-gpu-boot must run inside a Slurm allocation}"

job_id="$SLURM_JOB_ID"
host_name="$(hostname -s)"
socket="gpu-${job_id}"
session=zovllm
inner_tmux=(/usr/bin/tmux -L "$socket" -f "$HOME/.tmux.inner.conf")
state_dir="${PSC_GPU_STATE_DIR:-$HOME/.local/state/psc-gpu}"
route_dir="$state_dir/routes"
route_file="$route_dir/$job_id.route"
core_bin="${HPC_CORE_BIN:-$HOME/.local/bin}"
snapshot="$core_bin/psc-local-snapshot"
if [[ -n "${HPC_ALLOCATION_REQUEST_ID:-}" ]]; then
    PSC_GPU_STATE_DIR="$state_dir" "$core_bin/psc-allocation" bind "$HPC_ALLOCATION_REQUEST_ID" --job "$job_id"
fi
@BOOT_GUARD@
restore_status="${TMPDIR:-/tmp}/psc-gpu-restore-${job_id}.status"
restore_stamp="$(date +%Y%m%d-%H%M%S)"
restore_log="$HOME/logs/psc/local-restore_job-${job_id}_${restore_stamp}.log"
doctor_status="${TMPDIR:-/tmp}/psc-gpu-doctor-${job_id}.status"
doctor_log="$HOME/logs/psc/terminal-doctor_job-${job_id}_${restore_stamp}.log"

mkdir -p "$HOME/logs/psc"
rm -f "$restore_status"
"${inner_tmux[@]}" new-session -d -s zovllm -n zovllm-setup \
    /bin/bash --noprofile --norc
for key in HPC_CORE_BIN PSC_LOCAL_SNAPSHOT_ARCHIVE PSC_LOCAL_SNAPSHOT_READY_SECONDS PSC_GPU_AUTOSAVE_INTERVAL; do
    [[ -z "${!key:-}" ]] || "${inner_tmux[@]}" set-environment -g "$key" "${!key}"
done
end_time="$(scontrol show job "$job_id" -o | sed -n 's/.* EndTime=\([^ ]*\).*/\1/p')"
end_epoch="$(date -d "$end_time" +%s 2>/dev/null || true)"
[[ -z "$end_epoch" ]] || "${inner_tmux[@]}" set-environment -g HPC_SNAPSHOT_END_EPOCH "$end_epoch"

restore_command="set -o pipefail; { printf 'restore_start=%s host=%s job=%s local=%s\\n' \"\$(date -Is)\" \"\$(hostname -s)\" \"$job_id\" \"\${LOCAL:-unset}\"; if '$snapshot' restore; then printf 'restore_status=success restore_end=%s\\n' \"\$(date -Is)\"; printf success > '$restore_status'; else restore_rc=\$?; printf 'restore_status=failed restore_rc=%s restore_end=%s\\n' \"\$restore_rc\" \"\$(date -Is)\"; printf 'failed:%s' \"\$restore_rc\" > '$restore_status'; fi; } 2>&1 | tee -a '$restore_log'"
"${inner_tmux[@]}" send-keys -t zovllm:zovllm-setup -l "$restore_command"
"${inner_tmux[@]}" send-keys -t zovllm:zovllm-setup Enter

for ((attempt = 0; attempt < 360; attempt++)); do
    if [[ -s "$restore_status" ]]; then
        break
    fi
    sleep 5
done

if [[ ! -s "$restore_status" ]]; then
    echo "psc-gpu-boot: snapshot restore timed out; see $restore_log" >&2
    exit 1
fi

if [[ "$(<"$restore_status")" != success ]]; then
    echo "psc-gpu-boot: snapshot restore failed; see $restore_log" >&2
    exit 1
fi

if [[ "${PSC_BOOT_DOCTOR_DISABLED:-0}" != 1 ]]; then
rm -f "$doctor_status"
doctor_command="set -o pipefail; source '$HOME/.psc-local-env.sh'; if '$HOME/.local/bin/psc-gpu-doctor' 2>&1 | tee -a '$doctor_log'; then printf success > '$doctor_status'; else doctor_rc=\${PIPESTATUS[0]}; printf 'failed:%s' \"\$doctor_rc\" > '$doctor_status'; fi"
"${inner_tmux[@]}" send-keys -t zovllm:zovllm-setup -l "$doctor_command"
"${inner_tmux[@]}" send-keys -t zovllm:zovllm-setup Enter

for ((attempt = 0; attempt < 240; attempt++)); do
    [[ -s "$doctor_status" ]] && break
    sleep 0.5
done

if [[ ! -s "$doctor_status" || "$(<"$doctor_status")" != success ]]; then
    echo "psc-gpu-boot: terminal doctor failed; see $doctor_log" >&2
    exit 1
fi
fi

"${inner_tmux[@]}" new-window -d -a -t zovllm:0 -n zovllm-autosave \
    /bin/bash --noprofile --norc
autosave_command="exec env PATH='$core_bin:/usr/bin:/bin' '$snapshot' autosave ${PSC_GPU_AUTOSAVE_INTERVAL:-300} >> '$HOME/logs/psc/autosave-$job_id.log' 2>&1"
"${inner_tmux[@]}" send-keys -t zovllm:zovllm-autosave -l "$autosave_command"
"${inner_tmux[@]}" send-keys -t zovllm:zovllm-autosave Enter
"$snapshot" ready

# Keep a browsable unpacked copy of the snapshot on Ocean, so the work stays
# visible over a bare ssh once this allocation ends. Reads and writes network
# storage only; it never touches $LOCAL or the archives, so it cannot affect
# psc-local-snapshot restore. Every step is guarded because the allocation must
# survive a mirror failure -- the mirror is a convenience, the node is not.
if [[ "${PSC_GPU_MIRROR_DISABLED:-0}" != 1 && -x "$HOME/.local/bin/psc-local-mirror" ]]; then
    if "${inner_tmux[@]}" new-window -d -a -t zovllm:0 -n zovllm-mirror /bin/bash --noprofile --norc 2>/dev/null; then
        mirror_command="exec env PATH='$HOME/.local/bin:/usr/bin:/bin' '$HOME/.local/bin/psc-local-mirror' watch ${PSC_GPU_MIRROR_INTERVAL:-300}"
        "${inner_tmux[@]}" send-keys -t zovllm:zovllm-mirror -l "$mirror_command" 2>/dev/null || true
        "${inner_tmux[@]}" send-keys -t zovllm:zovllm-mirror Enter 2>/dev/null || true
    else
        echo "psc-gpu-boot: could not start zovllm-mirror; the snapshot mirror is disabled" >&2
    fi
fi

if [[ -n "$outer_socket" && -n "$outer_target" ]]; then
    umask 077
    mkdir -p "$route_dir"
    route_tmp="$route_file.tmp.$$"
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$job_id" "$host_name" "$outer_socket" "$outer_target" "$socket" \
        "$outer_pane_pid" > "$route_tmp"
    chmod 600 "$route_tmp"
    mv -f "$route_tmp" "$route_file"
else
    echo "psc-gpu-boot: outer tmux route is unavailable; psc-gpu run is disabled" >&2
fi

printf 'PSC_GPU_READY job=%s host=%s local=%s socket=%s route=%s\n' \
    "$job_id" "$host_name" "${LOCAL:-unset}" "$socket" "$outer_target"
if [[ -n "${HPC_ALLOCATION_REQUEST_ID:-}" ]]; then
    PSC_GPU_STATE_DIR="$state_dir" "$core_bin/psc-allocation" bind "$HPC_ALLOCATION_REQUEST_ID" --job "$job_id" --ready
fi
flock -u 8
exec 8>&-
"${inner_tmux[@]}" attach -t zovllm || true

# Keep the Slurm step alive after detaching so the allocation can be reattached.
while "${inner_tmux[@]}" has-session -t zovllm 2>/dev/null; do
    sleep 60
done
