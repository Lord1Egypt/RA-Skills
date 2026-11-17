#!/usr/bin/env bash
set -euo pipefail
config_file="${PSC_GPU_CONFIG:-$HOME/.config/psc-gpu/gpu.env}"
[[ ! -r "$config_file" ]] || source "$config_file"

state_dir="${PSC_GPU_STATE_DIR:-$HOME/.local/state/psc-gpu}"
route_dir="$state_dir/routes"
ack_dir="$state_dir/acks"
completion_dir="$state_dir/completions"
inner_runner="${PSC_GPU_INNER_RUNNER:-${HPC_CORE_BIN:-$HOME/.local/bin}/psc-gpu-inner-run}"
default_window="${PSC_GPU_DEFAULT_WINDOW:-zovllm-run}"
outer_label="${PSC_GPU_OUTER_LABEL:-psc-login}"
outer_session="${PSC_GPU_OUTER_SESSION:-psc-login}"
outer_window="${PSC_GPU_OUTER_WINDOW:-gpu-request}"

usage() {
    cat <<'EOF'
Usage:
  psc-gpu [GPU_TYPE] [GPU_COUNT] [WALLTIME] [BEGIN_TIME]
  psc-gpu run [--job JOB_ID] [--wait] [WINDOW] -- COMMAND [ARG...]
  psc-gpu run [--job JOB_ID] --request REQUEST_ID [--wait] WINDOW -- COMMAND [ARG...]
  psc-gpu task REQUEST_ID
  psc-gpu close [--job JOB_ID] WINDOW
  psc-gpu status

Defaults:
  GPU_COUNT  = 2
  WALLTIME   = 08:00:00
  BEGIN_TIME = optional Slurm start time, for example "10:00 08/25/26"

Requests H100 GPUs on GPU-shared and bootstraps the compute-node tmux,
snapshot restore, five-minute autosave, and the configured CUDA/GCC toolchain.
`psc-gpu run` only forwards commands to that existing tmux environment.
EOF
}

die() {
    echo "psc-gpu: $*" >&2
    exit 1
}

route_is_active() {
    local route_job="$1"
    local route_socket="$2"
    local route_target="$3"
    local route_pane_pid="${4:-}"
    local pane_dead pane_pid slurm_state

    # The route is registered once by psc-gpu-boot. Keep command dispatch on
    # the existing tmux bridge and do not query Slurm on every invocation or
    # completion poll; a slow controller must not delay a finished command.
    pane_dead="$(/usr/bin/tmux -S "$route_socket" display-message -p -t "$route_target" '#{pane_dead}' 2>/dev/null)" || return 1
    [[ "$pane_dead" == 0 ]] || return 1
    pane_pid="$(/usr/bin/tmux -S "$route_socket" display-message -p -t "$route_target" '#{pane_pid}' 2>/dev/null)" || return 1
    if [[ -n "$route_pane_pid" ]]; then
        [[ "$pane_pid" == "$route_pane_pid" ]]
        return
    fi

    # Compatibility for routes created before pane identity was recorded.
    slurm_state="$(/usr/bin/squeue -h -j "$route_job" -o '%T' 2>/dev/null | head -n 1 || true)"
    [[ "$slurm_state" == RUNNING ]]
}

collect_active_routes() {
    local requested_job="$1"
    local route_path route_job route_host route_socket route_target route_inner route_pane_pid
    local -a route_paths=()

    active_routes=()
    shopt -s nullglob
    route_paths=("$route_dir"/*.route)
    shopt -u nullglob

    for route_path in "${route_paths[@]}"; do
        IFS=$'\t' read -r route_job route_host route_socket route_target route_inner route_pane_pid < "$route_path" || continue
        [[ "$route_job" =~ ^[0-9]+$ ]] || continue
        [[ -z "$requested_job" || "$route_job" == "$requested_job" ]] || continue
        route_is_active "$route_job" "$route_socket" "$route_target" "$route_pane_pid" || continue
        active_routes+=("$route_job"$'\t'"$route_host"$'\t'"$route_socket"$'\t'"$route_target"$'\t'"$route_inner"$'\t'"$route_pane_pid")
    done
}

run_command() {
    local requested_job=""
    local window="$default_window"
    local window_set=false
    local wait_for_completion=false
    local command_string payload request_id='' ack_path status message dispatch_id
    local completion_path exit_code completed_job completed_window completed_at
    local selected_job selected_host selected_socket selected_target selected_inner selected_pane_pid
    local runner_shell tmux_command
    local dispatch_lock="$state_dir/dispatch.lock"
    local -a command_args=()

    while (($#)); do
        case "$1" in
            --request)
                request_id="$2"
                shift 2
                ;;
            --job)
                (($# >= 2)) || die "--job requires a job ID"
                requested_job="$2"
                shift 2
                ;;
            --wait)
                wait_for_completion=true
                shift
                ;;
            --window)
                (($# >= 2)) || die "--window requires a name"
                window="$2"
                window_set=true
                shift 2
                ;;
            --)
                shift
                break
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                [[ "$window_set" == false ]] || die "expected -- before command"
                window="$1"
                window_set=true
                shift
                [[ "${1:-}" == -- ]] || die "expected -- after window name"
                shift
                break
                ;;
        esac
    done

    (($# > 0)) || die "run requires a command"
    [[ -z "$requested_job" || "$requested_job" =~ ^[0-9]+$ ]] || die "invalid job ID: $requested_job"
    [[ "$window" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || die "invalid window name: $window"
    [[ -x "$inner_runner" ]] || die "inner runner is missing: $inner_runner"

    collect_active_routes "$requested_job"
    if ((${#active_routes[@]} == 0)); then
        if [[ -n "$requested_job" ]]; then
            die "job $requested_job has no active READY route"
        fi
        die "no active READY GPU node"
    fi
    if ((${#active_routes[@]} > 1)); then
        echo "psc-gpu: multiple active GPU nodes; choose one with --job:" >&2
        for status in "${active_routes[@]}"; do
            IFS=$'\t' read -r selected_job selected_host _ <<< "$status"
            printf '  %s  %s\n' "$selected_job" "$selected_host" >&2
        done
        exit 2
    fi

    IFS=$'\t' read -r selected_job selected_host selected_socket selected_target selected_inner selected_pane_pid <<< "${active_routes[0]}"
    command_args=("$@")
    printf -v command_string '%q ' "${command_args[@]}"
    command_string="${command_string% }"
    payload="$(printf '%s' "$command_string" | /usr/bin/base64 -w 0)"
    request_id="${request_id:-$(date +%s%N)-$$}"
    [[ "$request_id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]] || die 'invalid request ID'
    mkdir -p "$ack_dir"
    chmod 700 "$state_dir" "$ack_dir" 2>/dev/null || true
    dispatch_id="$(date +%s%N)-$$"
    ack_path="$ack_dir/$dispatch_id.ack"
    completion_path="$completion_dir/$request_id.done"

    printf -v runner_shell '%q ' /usr/bin/env "PSC_GPU_STATE_DIR=$state_dir" "$inner_runner" --job "$selected_job" --window "$window" --payload "$payload" --request "$request_id" --ack-request "$dispatch_id"
    runner_shell="${runner_shell% }"
    tmux_command="run-shell -b \"$runner_shell\""

    exec 9>"$dispatch_lock"
    /usr/bin/flock -w 10 9 || die "timed out waiting for the terminal dispatch lock"
    /usr/bin/tmux -S "$selected_socket" send-keys -t "$selected_target" C-b ':'
    sleep 0.1
    /usr/bin/tmux -S "$selected_socket" send-keys -t "$selected_target" -l "$tmux_command"
    /usr/bin/tmux -S "$selected_socket" send-keys -t "$selected_target" Enter

    for ((attempt = 0; attempt < 50; attempt++)); do
        [[ -s "$ack_path" ]] && break
        sleep 0.1
    done
    [[ -s "$ack_path" ]] || die "dispatch timed out for job $selected_job on $selected_host"

    IFS=$'\t' read -r status message < "$ack_path"
    /usr/bin/flock -u 9
    [[ "$status" == ok ]] || die "$message"
    printf '%s:%s request=%s\n' "$selected_host" "$window" "$request_id"

    if [[ "$wait_for_completion" == true ]]; then
        while [[ ! -s "$completion_path" ]]; do
            route_is_active "$selected_job" "$selected_socket" "$selected_target" "$selected_pane_pid" || \
                die "job $selected_job ended before request $request_id completed"
            sleep 0.2
        done
        IFS=$'\t' read -r exit_code completed_job completed_window completed_at < "$completion_path"
        [[ "$exit_code" =~ ^[0-9]+$ ]] || die "invalid completion record for request $request_id"
        printf 'completed job=%s window=%s exit=%s at=%s\n' \
            "$completed_job" "$completed_window" "$exit_code" "$completed_at"
        [[ ! -f "$state_dir/requests/$request_id/output.log" ]] || cat "$state_dir/requests/$request_id/output.log"
        return "$exit_code"
    fi
}

close_window() {
    local requested_job=""
    local window=""
    local request_id ack_path status message
    local selected_job selected_host selected_socket selected_target selected_inner selected_pane_pid
    local runner_shell tmux_command
    local dispatch_lock="$state_dir/dispatch.lock"

    while (($#)); do
        case "$1" in
            --job)
                (($# >= 2)) || die "--job requires a job ID"
                requested_job="$2"
                shift 2
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                [[ -z "$window" ]] || die "close accepts one window name"
                window="$1"
                shift
                ;;
        esac
    done

    [[ -n "$window" ]] || die "close requires a window name"
    [[ -z "$requested_job" || "$requested_job" =~ ^[0-9]+$ ]] || die "invalid job ID: $requested_job"
    [[ "$window" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || die "invalid window name: $window"

    collect_active_routes "$requested_job"
    ((${#active_routes[@]} > 0)) || die "no active READY GPU node"
    if ((${#active_routes[@]} > 1)); then
        die "multiple active GPU nodes; choose one with --job"
    fi

    IFS=$'\t' read -r selected_job selected_host selected_socket selected_target selected_inner selected_pane_pid <<< "${active_routes[0]}"
    request_id="$(date +%s%N)-$$"
    mkdir -p "$ack_dir"
    chmod 700 "$state_dir" "$ack_dir" 2>/dev/null || true
    ack_path="$ack_dir/$request_id.ack"

    printf -v runner_shell '%q ' "$inner_runner" --job "$selected_job" --window "$window" --request "$request_id" --close
    runner_shell="${runner_shell% }"
    tmux_command="run-shell -b \"$runner_shell\""

    exec 9>"$dispatch_lock"
    /usr/bin/flock -w 10 9 || die "timed out waiting for the terminal dispatch lock"
    /usr/bin/tmux -S "$selected_socket" send-keys -t "$selected_target" C-b ':'
    sleep 0.1
    /usr/bin/tmux -S "$selected_socket" send-keys -t "$selected_target" -l "$tmux_command"
    /usr/bin/tmux -S "$selected_socket" send-keys -t "$selected_target" Enter

    for ((attempt = 0; attempt < 50; attempt++)); do
        [[ -s "$ack_path" ]] && break
        sleep 0.1
    done
    [[ -s "$ack_path" ]] || die "close timed out for job $selected_job on $selected_host"
    IFS=$'\t' read -r status message < "$ack_path"
    /usr/bin/flock -u 9
    [[ "$status" == ok ]] || die "$message"
    printf '%s:%s closed\n' "$selected_host" "$window"
}

show_status() {
    local route_path route_job route_host route_socket route_target route_inner route_pane_pid state
    local -a route_paths=()

    shopt -s nullglob
    route_paths=("$route_dir"/*.route)
    shopt -u nullglob
    if ((${#route_paths[@]} == 0)); then
        echo "No registered PSC GPU routes."
        return 0
    fi

    printf 'JOB_ID\tHOST\tSTATE\n'
    for route_path in "${route_paths[@]}"; do
        IFS=$'\t' read -r route_job route_host route_socket route_target route_inner route_pane_pid < "$route_path" || continue
        state="$(/usr/bin/squeue -h -j "$route_job" -o '%T' 2>/dev/null | head -n 1 || true)"
        [[ -n "$state" ]] || state=INACTIVE
        printf '%s\t%s\t%s\n' "$route_job" "$route_host" "$state"
    done
}

request_gpu() {
    local allocation_request=""
    [[ "${allocation_internal:-0}" != 1 ]] || allocation_request="${HPC_ALLOCATION_REQUEST_ID:-}"
    if [[ "${1:-}" == --request ]]; then
        (($# >= 2)) || die '--request requires an ID'
        allocation_request="$2"; shift 2
    fi
    allocation_request="${allocation_request:-$(date +%s%N)-$$}"
    local -a original_args=("$@")
    local gpu_type=h100 gpu_gres=h100-80 gpu_partition=GPU-shared gpu_pattern=H100 gpu_qos=""
    if [[ "${1:-}" =~ ^(h100|a100|l40s|v100)$ ]]; then
        gpu_type="$1"
        shift
    fi
    case "$gpu_type" in
        a100) gpu_gres=a100; gpu_partition=GPU-dev; gpu_pattern=A100; gpu_qos=gpudevinteract ;;
        l40s) gpu_gres=l40s-48; gpu_pattern=L40S ;;
        v100) gpu_gres=v100-32; gpu_pattern=V100 ;;
    esac
    export PSC_GPU_EXPECTED_GPU_NAME_PATTERN="$gpu_pattern"
    gpu_partition="${PSC_GPU_PARTITION:-$gpu_partition}"
    gpu_qos="${PSC_GPU_QOS:-$gpu_qos}"
    local gpu_count="${1:-2}"
    local walltime="${2:-08:00:00}"
    local begin_time="${3:-}"
    local outer_socket outer_target current_socket current_target pane_command pane_pid
    local delegated_command
    local -a salloc_args=(
        "--job-name=${HPC_CORE_JOB_NAME:-psc-gpu}"
        "--partition=$gpu_partition"
        --nodes=1
        --gres="gpu:${gpu_gres}:${gpu_count}"
        --time="$walltime"
    )

    (($# <= 3)) || die "too many allocation arguments"
    [[ -z "${PSC_ACCOUNT:-}" ]] || salloc_args+=("--account=$PSC_ACCOUNT")
    [[ -z "${PSC_CPUS_PER_TASK:-}" ]] || salloc_args+=("--cpus-per-task=$PSC_CPUS_PER_TASK")
    [[ -z "${PSC_MEMORY:-}" ]] || salloc_args+=("--mem=$PSC_MEMORY")
    [[ -z "${HPC_ALLOCATION_COMMENT:-}" ]] || salloc_args+=("--comment=$HPC_ALLOCATION_COMMENT")
    [[ -z "$gpu_qos" ]] || salloc_args+=("--qos=$gpu_qos")
    [[ "$gpu_type" != a100 || "$gpu_count" == 1 ]] || die "GPU-dev A100 requires one GPU"
    [[ "$gpu_count" == 1 || "$gpu_count" == 2 || "$gpu_count" == 4 || "$gpu_count" == 8 ]] || \
        die "GPU_COUNT must be one of 1, 2, 4, or 8"
    [[ "$walltime" =~ ^[0-9]+:[0-5][0-9]:[0-5][0-9]$ ]] || \
        die "WALLTIME must use HH:MM:SS"

    if [[ -n "$begin_time" ]]; then
        salloc_args+=(--begin="$begin_time")
    fi

    current_socket="${TMUX:-}"
    current_socket="${current_socket%%,*}"
    current_target=""
    # The calling pane, not the server's active pane, owns this allocation.
    if [[ -n "$current_socket" && -n "${TMUX_PANE:-}" ]]; then
        current_target="$(/usr/bin/tmux -S "$current_socket" display-message -p \
            -t "$TMUX_PANE" '#{session_name}:#{window_name}.#{pane_index}')"
    fi

    if [[ "${allocation_internal:-0}" != 1 ]]; then
        if ! /usr/bin/tmux -L "$outer_label" has-session -t "$outer_session" 2>/dev/null; then
            /usr/bin/tmux -L "$outer_label" -f "$HOME/.tmux.conf" \
                new-session -d -s "$outer_session" -n "$outer_window" \
                /bin/bash --noprofile --norc
        elif ! /usr/bin/tmux -L "$outer_label" list-windows -t "$outer_session" \
                -F '#{window_name}' | /usr/bin/grep -Fxq "$outer_window"; then
            /usr/bin/tmux -L "$outer_label" new-window -d -t "$outer_session" \
                -n "$outer_window" /bin/bash --noprofile --norc
        fi

        # Detached panes can inherit a previous allocation's route and defaults.
        # Carry the requested outer identity explicitly and rebuild route metadata
        # only after the delegated process identifies its own pane.
        local -a core_env=()
        local key
        for key in HPC_CORE_BIN HPC_CORE_JOB_NAME PSC_GPU_CONFIG PSC_ACCOUNT PSC_CPUS_PER_TASK PSC_MEMORY PSC_GPU_PARTITION PSC_GPU_QOS PSC_LOCAL_SNAPSHOT_ARCHIVE PSC_GPU_AUTOSAVE_INTERVAL PSC_GPU_MIRROR_DISABLED PSC_LOCAL_SNAPSHOT_READY_SECONDS; do
            [[ -z "${!key:-}" ]] || core_env+=("$key=${!key}")
        done
        PSC_GPU_STATE_DIR="$state_dir" "${HPC_CORE_BIN:-$HOME/.local/bin}/psc-allocation" submit "$allocation_request" \
            --socket "$outer_label" --target "$outer_session:$outer_window" \
            --field "gpu=$gpu_gres" --field "partition=$gpu_partition" --field "qos=$gpu_qos" \
            --field "account=${PSC_ACCOUNT:-}" --field "cpus=${PSC_CPUS_PER_TASK:-}" --field "memory=${PSC_MEMORY:-}" \
            --field "count=$gpu_count" --field "time=$walltime" --field "begin=$begin_time" \
            --field "job_name=${HPC_CORE_JOB_NAME:-}" \
            -- /usr/bin/env \
            -u PSC_GPU_OUTER_SOCKET -u PSC_GPU_OUTER_TARGET -u PSC_GPU_OUTER_PANE_PID \
            "${core_env[@]}" \
            "PSC_GPU_OUTER_LABEL=$outer_label" \
            "PSC_GPU_OUTER_SESSION=$outer_session" \
            "PSC_GPU_OUTER_WINDOW=$outer_window" \
            "PSC_GPU_STATE_DIR=$state_dir" \
            "${HPC_CORE_BIN:-$HOME/.local/bin}/psc-gpu" _allocate "${original_args[@]}"
        return 0
    fi

    [[ "$current_socket" == */"$outer_label" && "$current_target" == "${outer_session}:${outer_window}."* ]] || \
        die 'internal allocation must run in its named allocation pane'

    outer_socket="$current_socket"
    outer_target="$current_target"
    export PSC_GPU_OUTER_SOCKET="$outer_socket"
    export PSC_GPU_OUTER_TARGET="$outer_target"
    export PSC_GPU_OUTER_PANE_PID
    PSC_GPU_OUTER_PANE_PID="$(/usr/bin/tmux -S "$current_socket" display-message -p \
        -t "$TMUX_PANE" '#{pane_pid}')"

    mkdir -p "$state_dir/allocations"
    # The durable holder tees the controlling PTY into this request log.
    # A stdout pipe here would disable srun --pty and break the terminal bridge.
    local allocation_log="$state_dir/allocations/${HPC_ALLOCATION_REQUEST_ID:?durable holder required}.log"
    printf 'GPU_REQUEST host=%s type=%s count=%s walltime=%s log=%s\n' \
        "$(hostname -s)" "$gpu_type" "$gpu_count" "$walltime" "$allocation_log"
    exec /usr/bin/salloc "${salloc_args[@]}" \
        /usr/bin/srun --pty --export=ALL "${HPC_CORE_BIN:-$HOME/.local/bin}/psc-gpu-boot"
}

case "${1:-}" in
    _allocate) allocation_internal=1; shift; request_gpu "$@" ;;
    allocation) shift; exec "${HPC_CORE_BIN:-$HOME/.local/bin}/psc-allocation" get "$@" ;;
    task)
        shift
        exec "$HOME/.local/bin/psc-agent-state" task "$@"
        ;;
    run)
        shift
        run_command "$@"
        ;;
    close)
        shift
        close_window "$@"
        ;;
    status)
        shift
        (($# == 0)) || die "status takes no arguments"
        show_status
        ;;
    help|-h|--help)
        usage
        ;;
    *)
        request_gpu "$@"
        ;;
esac
