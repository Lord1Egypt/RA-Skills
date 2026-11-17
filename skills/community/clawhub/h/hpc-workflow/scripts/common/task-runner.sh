#!/usr/bin/env bash
# Generated site adapter: shared request identity, locking and execution rules.
set -euo pipefail
umask 077
site='@SITE@'
adapter='@ADAPTER@'
state_dir="${@PREFIX@_GPU_STATE_DIR:-$HOME/.local/state/$site-gpu}"
job_id='' window='' payload='' request_id='' ack_request='' mode=run wait_for_completion=false
while (($#)); do
    case "$1" in
        --job) job_id="$2"; shift 2 ;;
        --window) window="$2"; shift 2 ;;
        --payload) payload="$2"; shift 2 ;;
        --request) request_id="$2"; shift 2 ;;
        --ack-request) ack_request="$2"; shift 2 ;;
        --close) mode=close; shift ;;
        --wait) wait_for_completion=true; shift ;;
        *) exit 2 ;;
    esac
done
[[ "$job_id" =~ ^[0-9]+$ && "$window" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
request_id="${request_id:-$(date +%s%N)-$$}"
[[ "$request_id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]] || exit 2
ack_request="${ack_request:-$request_id}"
[[ "$ack_request" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]] || exit 2
session=work
conf="$HOME/.config/@SITE@-gpu/tmux.compute.conf"
workspace="${@PREFIX@_WORKSPACE:-$HOME}"
if [[ "$adapter" == psc ]]; then
    session=zovllm; conf="$HOME/.tmux.inner.conf"; workspace="${LOCAL:-$HOME}"
fi
socket="gpu-$job_id"
inner_tmux=(/usr/bin/tmux -L "$socket" -f "$conf")
target="$session:$window"
request_dir="$state_dir/requests/$request_id"
mkdir -p "$state_dir/requests" "$state_dir/acks" "$state_dir/completions" "$state_dir/commands"
write_ack() {
    printf '%s\t%s\n' "$1" "$2" > "$state_dir/acks/$ack_request.ack.tmp.$$"
    mv -f "$state_dir/acks/$ack_request.ack.tmp.$$" "$state_dir/acks/$ack_request.ack"
}
fail() { write_ack error "$*"; echo "$*" >&2; exit 1; }
case "$window" in setup|autosave|zovllm-setup|zovllm-autosave|zovllm-mirror) fail 'protected window' ;; esac
"${inner_tmux[@]}" has-session -t "$session" || fail 'inner tmux unavailable'
workspace_key=@PREFIX@_WORKSPACE
[[ "$adapter" != psc ]] || workspace_key=LOCAL
workspace_record="$("${inner_tmux[@]}" show-environment -g "$workspace_key" 2>/dev/null || true)"
[[ "$workspace_record" != "$workspace_key="* ]] || workspace="${workspace_record#*=}"
allocation_id="$("${inner_tmux[@]}" show-environment -g SLURM_JOB_ID)"
[[ "${allocation_id#SLURM_JOB_ID=}" == "$job_id" ]] || fail 'allocation identity mismatch'
[[ -z "${SLURM_JOB_ID:-}" || "$SLURM_JOB_ID" == "$job_id" ]] || fail 'caller allocation identity mismatch'
# The lock covers reservation, window creation and dispatch, including close.
exec 9>"$state_dir/task-dispatch.lock"
flock -w 15 9 || fail 'task dispatch lock timeout'
if [[ "$mode" == close ]]; then
    case "$window" in setup|autosave|zovllm-setup|zovllm-autosave|zovllm-mirror) fail 'protected window' ;; esac
    pane_pid="$("${inner_tmux[@]}" display-message -p -t "$target" '#{pane_pid}')"
    busy="$("${inner_tmux[@]}" show-options -wqv -t "$target" @hpc_gpu_busy)"
    [[ "$busy" != 1 ]] && ! pgrep -P "$pane_pid" >/dev/null || fail 'window busy'
    "${inner_tmux[@]}" kill-window -t "$target"
    write_ack ok "closed $target"; exit 0
fi
[[ -n "$payload" ]] || fail 'empty payload'
command_string="$(printf %s "$payload" | base64 --decode)" || fail 'invalid payload'
if [[ -e "$request_dir/identity" ]]; then
    expected="$(printf '%s\t%s\t%s' "$job_id" "$window" "$payload")"
    [[ "$(cat "$request_dir/identity")" == "$expected" ]] || fail 'request ID reused with different job/window/command'
    # An uncertain dispatch is never retried automatically.
    write_ack ok "existing request $request_id; inspect task record"
else
    if "${inner_tmux[@]}" list-windows -t "$session" -F '#{window_name}' | grep -Fxq "$window"; then
        pane_pid="$("${inner_tmux[@]}" display-message -p -t "$target" '#{pane_pid}')"
        pane_command="$("${inner_tmux[@]}" display-message -p -t "$target" '#{pane_current_command}')"
        busy="$("${inner_tmux[@]}" show-options -wqv -t "$target" @hpc_gpu_busy)"
        [[ "$busy" != 1 && "$pane_command" == bash ]] && ! pgrep -P "$pane_pid" >/dev/null || fail 'window busy'
    else
        "${inner_tmux[@]}" new-window -d -t "$session:" -n "$window" -c "$workspace" /bin/bash --noprofile --norc
    fi
    mkdir -p "$request_dir"
    printf '%s\t%s\t%s\n' "$job_id" "$window" "$payload" > "$request_dir/identity"
    printf '%s\n' "$command_string" > "$request_dir/command.txt"
    printf 'reserved\t%s\n' "$(date -Is)" > "$request_dir/state"
    command_path="$state_dir/commands/$request_id.sh"
    {
        printf '#!/usr/bin/env bash\nset +e\n'
        for key in request_dir request_id job_id window site socket target state_dir; do printf '%s=%q\n' "$key" "${!key}"; done
        cat <<'WORKER'
finish_task() {
    rc=$?; trap - EXIT
    printf 'completed\t%s\t%s\n' "$(date -Is)" "$rc" > "$request_dir/state.tmp"
    mv -f "$request_dir/state.tmp" "$request_dir/state"
    if [[ "$site" == psc ]]; then
        printf '%s\t%s\t%s\t%s\n' "$rc" "$job_id" "$window" "$(date -Is)" > "$state_dir/completions/$request_id.done.tmp"
    else
        printf '%s\t%s\n' "$rc" "$(date -Is)" > "$state_dir/completions/$request_id.done.tmp"
    fi
    mv -f "$state_dir/completions/$request_id.done.tmp" "$state_dir/completions/$request_id.done"
    tmux -L "$socket" set-option -w -t "$target" @hpc_gpu_busy 0 2>/dev/null || true
    tmux -L "$socket" set-option -w -t "$target" @psc_gpu_busy 0 2>/dev/null || true
    exit "$rc"
}
trap finish_task EXIT
printf 'running\t%s\n' "$(date -Is)" > "$request_dir/state.tmp"
mv -f "$request_dir/state.tmp" "$request_dir/state"
# Both terminal output and a persistent file retain the command's real status.
set -o pipefail
bash --noprofile --norc "$request_dir/command.txt" 2>&1 | tee -a "$request_dir/output.log"
codes=("${PIPESTATUS[@]}")
rc="${codes[0]}"
[[ "$rc" != 0 ]] || rc="${codes[1]}"
exit "$rc"
WORKER
    } > "$command_path"
    chmod 700 "$command_path"
    "${inner_tmux[@]}" set-option -w -t "$target" @hpc_gpu_busy 1
    "${inner_tmux[@]}" set-option -w -t "$target" @psc_gpu_busy 1
    printf -v dispatch 'bash %q' "$command_path"
    "${inner_tmux[@]}" send-keys -t "$target" -l "$dispatch" || fail 'dispatch uncertain; inspect request before retry'
    "${inner_tmux[@]}" send-keys -t "$target" Enter || fail 'dispatch uncertain; inspect request before retry'
    write_ack ok "dispatched $target request=$request_id"
fi
flock -u 9
printf 'dispatched job=%s window=%s request=%s\n' "$job_id" "$window" "$request_id"
if [[ "$wait_for_completion" == true ]]; then
    while [[ ! -s "$state_dir/completions/$request_id.done" ]]; do
        "${inner_tmux[@]}" has-session -t "$session" || fail 'allocation ended; task outcome unknown'
        sleep 0.2
    done
    read -r rc _ < "$state_dir/completions/$request_id.done"
    [[ ! -f "$request_dir/output.log" ]] || cat "$request_dir/output.log"
    exit "$rc"
fi
