#!/usr/bin/env bash
# Generic Slurm adapter for sites with login-to-compute SSH access.
set -euo pipefail
config="${@PREFIX@_GPU_CONFIG:-$HOME/.config/@SITE@-gpu/gpu.env}"
set -a; source "$config"; set +a
core_bin="${HPC_CORE_BIN:-$HOME/.local/bin}"
state="${@PREFIX@_GPU_STATE_DIR:-$HOME/.local/state/@SITE@-gpu}"
export @PREFIX@_GPU_STATE_DIR="$state"
die() { echo '@SITE@-gpu: '"$*" >&2; exit 2; }
case "${1:-}" in
  allocation) shift; exec "$core_bin/@SITE@-allocation" get "$@" ;;
  status|doctor) mode="$1"; shift; [[ "${1:-}" != --json ]] || shift; exec "$core_bin/@SITE@-agent-state" "$mode" "$@" ;;
  task) shift; exec "$core_bin/@SITE@-agent-state" task "$@" ;;
  run)
    shift; job='' request='' wait_flag='' window=''
    while (($#)); do
      case "$1" in
        --job) job="$2"; shift 2 ;;
        --request) request="$2"; shift 2 ;;
        --wait) wait_flag=--wait; shift ;;
        *) window="$1"; shift; [[ "${1:-}" == -- ]] || die 'run requires WINDOW -- COMMAND'; shift; break ;;
      esac
    done
    [[ "$job" =~ ^[0-9]+$ && -n "$window" && $# -gt 0 ]] || die 'run requires --job ID and WINDOW -- COMMAND'
    IFS=$'\t' read -r route_job host socket session < "$state/routes/$job.route"
    [[ "$route_job" == "$job" && "$host" =~ ^[A-Za-z0-9][A-Za-z0-9.-]*$ ]] || die 'invalid route'
    phase="$(squeue -h -u "$USER" -j "$job" -o '%T')" || die 'scheduler state unknown'
    [[ "$phase" == RUNNING ]] || die 'allocation is not running'
    printf -v command '%q ' "$@"
    payload="$(printf '%s' "${command% }" | base64 -w 0)"
    request="${request:-$(date +%s%N)-$$}"
    printf -v remote '%q ' /usr/bin/env "@PREFIX@_GPU_STATE_DIR=$state" "$core_bin/@SITE@-gpu-inner-run" --job "$job" --window "$window" --request "$request" --payload "$payload" ${wait_flag:+$wait_flag}
    exec ssh -o BatchMode=yes -o ConnectTimeout=10 "$host" "${remote% }"
    ;;
  _allocate)
    shift
    [[ -n "${HPC_ALLOCATION_REQUEST_ID:-}" && -n "${HPC_ALLOCATION_COMMENT:-}" ]] || die 'internal allocation identity missing'
    type="$1" count="$2" walltime="$3" begin="${4:-}"
    args=("--account=$HPC_ACCOUNT" "--partition=${HPC_GPU_PARTITION[$type]}" --nodes=1 --ntasks=1
      "--cpus-per-task=$HPC_CPUS" "--mem=$HPC_MEMORY" "--gres=gpu:${HPC_GPU_GRES[$type]}:$count"
      "--time=$walltime" "--job-name=$HPC_CORE_JOB_NAME" "--comment=$HPC_ALLOCATION_COMMENT")
    [[ -z "${HPC_GPU_QOS[$type]}" ]] || args+=("--qos=${HPC_GPU_QOS[$type]}")
    [[ -z "${HPC_LOCAL_SCRATCH_REQUEST:-}" ]] || args+=("--tmp=$HPC_LOCAL_SCRATCH_REQUEST")
    [[ -z "$begin" ]] || args+=("--begin=$begin")
    exec salloc "${args[@]}" srun --pty --export=ALL "$core_bin/@SITE@-gpu-boot"
    ;;
esac
request=''
if [[ "${1:-}" == --request ]]; then request="$2"; shift 2; fi
request="${request:-$(date +%s%N)-$$}"
type="${1:-$HPC_DEFAULT_GPU}"; count="${2:-1}"; walltime="${3:-$HPC_WALLTIME}"; begin="${4:-}"
(($# <= 4)) || die 'too many arguments'
[[ -n "${HPC_GPU_GRES[$type]:-}" ]] || die 'GPU type absent from verified site profile'
[[ "$count" =~ ^[1-9][0-9]*$ && "$count" -le "${HPC_GPU_MAX_COUNT[$type]}" ]] || die 'invalid GPU count'
[[ "$walltime" =~ ^[0-9]+:[0-5][0-9]:[0-5][0-9]$ ]] || die 'invalid walltime'
outer=(tmux -L "$HPC_OUTER_SOCKET")
if ! "${outer[@]}" has-session -t "$HPC_OUTER_SESSION" 2>/dev/null; then
  "${outer[@]}" new-session -d -s "$HPC_OUTER_SESSION" -n control /bin/bash --noprofile --norc
fi
if ! "${outer[@]}" list-windows -t "$HPC_OUTER_SESSION" -F '#{window_name}' | grep -Fxq gpu-request; then
  "${outer[@]}" new-window -d -t "$HPC_OUTER_SESSION:" -n gpu-request /bin/bash --noprofile --norc
fi
exec "$core_bin/@SITE@-allocation" submit "$request" --socket "$HPC_OUTER_SOCKET" --target "$HPC_OUTER_SESSION:gpu-request" \
  --field "account=$HPC_ACCOUNT" --field "gpu=${HPC_GPU_GRES[$type]}" --field "partition=${HPC_GPU_PARTITION[$type]}" \
  --field "qos=${HPC_GPU_QOS[$type]}" --field "count=$count" --field "time=$walltime" --field "begin=$begin" \
  --field "cpus=$HPC_CPUS" --field "memory=$HPC_MEMORY" --field "scratch=${HPC_LOCAL_SCRATCH_REQUEST:-}" \
  --field "profile_hash=$HPC_PROFILE_HASH" \
  -- /usr/bin/env "@PREFIX@_GPU_CONFIG=$config" "HPC_CORE_BIN=$core_bin" "@PREFIX@_GPU_STATE_DIR=$state" \
  "$core_bin/@SITE@-gpu" _allocate "$type" "$count" "$walltime" "$begin"
