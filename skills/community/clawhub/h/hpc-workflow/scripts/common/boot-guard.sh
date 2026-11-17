# Shared bootstrap guard, embedded into each site helper by build.py.
umask 077
mkdir -p "$state_dir"
exec 8>"$state_dir/bootstrap-$job_id.lock"
flock -w 15 8 || { echo 'bootstrap already in progress' >&2; exit 3; }
if "${inner_tmux[@]}" has-session -t "$session" 2>/dev/null; then
    recorded_job="$("${inner_tmux[@]}" show-environment -g SLURM_JOB_ID 2>/dev/null || true)"
    if [[ "${recorded_job#SLURM_JOB_ID=}" == "$job_id" && -s "$route_file" ]] &&
            [[ "$(cut -f1 "$route_file")" == "$job_id" && "$(cut -f2 "$route_file")" == "$host_name" ]]; then
        printf 'GPU_BOOT_REUSED job=%s host=%s session=%s\n' "$job_id" "$host_name" "$session"
        exit 0
    fi
    echo 'existing compute session has no matching READY route; preserved for inspection' >&2
    exit 3
fi
if "${inner_tmux[@]}" list-sessions >/dev/null 2>&1; then
    echo 'unexpected sessions on job socket; preserved for inspection' >&2
    exit 3
fi
