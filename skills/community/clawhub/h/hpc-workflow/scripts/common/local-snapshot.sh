#!/usr/bin/env bash
set -euo pipefail

# Node-local workspace snapshots for MSI, ported from PSC's psc-local-snapshot.
# The local base lives on job-scoped /scratch.local and disappears with the job;
# the archive lives on networked home storage and survives it. A full snapshot
# plus an ordered chain of incremental packs keeps the five-minute autosave
# cheap even when the base holds tens of gigabytes.

usage() {
    cat <<'EOF'
Usage:
  @SITE@-local-snapshot restore [ARCHIVE]
  @SITE@-local-snapshot verify [ARCHIVE]
  @SITE@-local-snapshot ready [ARCHIVE]
  @SITE@-local-snapshot rebaseline [ARCHIVE]
  @SITE@-local-snapshot save [ARCHIVE]
  @SITE@-local-snapshot incsave [ARCHIVE]
  @SITE@-local-snapshot compact [ARCHIVE]
  @SITE@-local-snapshot autosave [SECONDS] [ARCHIVE]
  @SITE@-local-snapshot start [SECONDS] [ARCHIVE]
  @SITE@-local-snapshot stop [ARCHIVE]
  @SITE@-local-snapshot log [ARCHIVE]
  @SITE@-local-snapshot status [ARCHIVE]
  @SITE@-local-snapshot path

Defaults:
  ARCHIVE = ~/.local/share/@SITE@-local-snapshot/workspace.tar.zst
  local   = $@PREFIX@_LOCAL_BASE, or /scratch.local/$USER/msi-codex

Examples:
  @SITE@-local-snapshot restore
  @SITE@-local-snapshot autosave 300
  @SITE@-local-snapshot save

Notes:
  save/compact writes a full packed snapshot and resets the incremental chain.
  incsave writes one packed incremental tar.zst next to the full snapshot.
  autosave writes incrementals at SECONDS and compacts every six hours by default.
  start/stop manages autosave in the background with a pid file and log.
  restore applies the full snapshot and all incremental packs in order, then
  rebuilds the incremental baseline for the new local filesystem.
  Snapshots include the uv cache under cache/uv but exclude every .venv, all
  other cache directories, and the local tmp directory. Keep pyproject.toml and
  uv.lock current, then run "uv sync --locked" after restore to recreate
  project environments.
  Existing full snapshots and incremental chains are moved aside only after the
  new full snapshot has been written and verified.

Environment:
  @PREFIX@_LOCAL_SNAPSHOT_COMPACT_SECONDS=21600
  @PREFIX@_LOCAL_SNAPSHOT_GENERATIONS_KEEP=3
  @PREFIX@_LOCAL_SNAPSHOT_END_MARGIN=120
  @PREFIX@_LOCAL_SNAPSHOT_MAX_INCREMENTAL_RATIO=50
EOF
}

die() {
    echo "@SITE@-local-snapshot: $*" >&2
    exit 1
}

local_base() {
    local base
    if [[ '@ADAPTER@' == msi ]]; then
        base="${@PREFIX@_LOCAL_BASE:-/scratch.local/$USER/msi-codex}"
        local prefix="${HPC_ALLOWED_LOCAL_PREFIX:-/scratch.local/$USER/}"
        [[ "$prefix" == /*/ && "$prefix" != / && "$base" == "$prefix"* && "$base" != *'/../'* ]] ||
            die "refusing unexpected local base: $base"
    else
        base="${LOCAL:-/local/slurm-${SLURM_JOB_ID:?allocation required}/local}"
        local prefix="${HPC_ALLOWED_LOCAL_PREFIX:-/local/}"
        [[ "$prefix" == /*/ && "$prefix" != / && "$base" == "$prefix"* && -d "$base" && -w "$base" ]] ||
            die "no writable job-scoped PSC local disk: $base"
    fi
    printf '%s\n' "$base"
}

ensure_base() {
    local base
    base="$(local_base)" || return $?
    local uv_relative=cache/uv
    [[ '@ADAPTER@' != psc ]] || uv_relative="cache/$USER/uv"
    mkdir -p "$base/workspace" "$base/$uv_relative" "$base/tmp" || return $?
    printf '%s\n' "$base"
}

archive_path() {
    local default_archive="$HOME/.local/share/@SITE@-local-snapshot/workspace.tar.zst"
    [[ '@ADAPTER@' != psc ]] || default_archive="$HOME/project/local-workspaces/local-$USER.tar.zst"
    local archive="${1:-${@PREFIX@_LOCAL_SNAPSHOT_ARCHIVE:-$default_archive}}"
    mkdir -p "$(dirname "$archive")"
    cd "$(dirname "$archive")"
    printf '%s/%s\n' "$(pwd)" "$(basename "$archive")"
}

incremental_dir() {
    printf '%s.inc\n' "$1"
}

autosave_pid_path() {
    printf '%s.autosave.pid\n' "${1%.tar.zst}"
}

autosave_log_path() {
    printf '%s.autosave.log\n' "${1%.tar.zst}"
}

write_autosave_identity() {
    local start
    start="$(awk '{print $22}' /proc/$$/stat)"
    printf '%s\t%s\t%s\n' "$$" "$(hostname)" "$start" > "$1.tmp.$$"
    mv -f "$1.tmp.$$" "$1"
}

read_autosave_identity() {
    local recorded_host recorded_start current_start
    IFS=$'\t' read -r pid recorded_host recorded_start < "$1" || return 1
    [[ "$pid" =~ ^[0-9]+$ && -n "$recorded_start" ]] || return 1
    [[ "$recorded_host" == "$(hostname)" ]] || return 1
    [[ -r "/proc/$pid/stat" ]] || return 1
    current_start="$(awk '{print $22}' "/proc/$pid/stat")"
    [[ "$current_start" == "$recorded_start" ]]
}

lock_dir() {
    printf '%s.lock\n' "$1"
}

with_lock() {
    local archive="$1"
    shift
    local lock status operation_functions health_assignment
    lock="${archive}.core.lock"
    # Copy only snapshot functions, not unrelated exported login-shell helpers.
    operation_functions="$(declare -f die local_base ensure_base archive_path \
        incremental_dir tar_excludes write_tar_roots make_stage_dir \
        copy_large_atomic verify_pack snapshot_budget prune_backups reset_incremental_baseline \
        rebaseline_cmd restore_cmd save_cmd compact_cmd incsave_cmd snapshot_health \
        generation_metadata generation_identity generation_select generation_clone \
        generation_publish transaction_cmd "$1")"
    printf -v health_assignment '%q' "$archive"
    set +e
    # A fresh Bash process also preserves errexit when autosave calls this
    # function from an if/|| context, where Bash disables it in subshells.
    # The kernel owns lock lifetime. Never infer remote lock ownership from PID.
    local -a restore_guard=()
    if [[ "$1" == transaction_cmd && "${2:-}" == restore ]]; then
        # A new allocation must not replace the baseline of a live writer.
        restore_guard=(flock -n "$archive.autosave.core.lock")
    fi
    "${restore_guard[@]}" flock -w "${@PREFIX@_LOCAL_SNAPSHOT_LOCK_SECONDS:-120}" "$lock" \
        "$BASH" -euo pipefail -c "$operation_functions; operation=\$1; health_archive=$health_assignment; trap 'rc=\$?; snapshot_health \"\$health_archive\" \"\$operation\" \"\$rc\" || true; exit \"\$rc\"' EXIT; \"\$@\"" -- "$@"
    status=$?
    set -e
    return "$status"
}

snapshot_health() {
    python3 - "$1" "$2" "$3" '@SITE@' <<'PY'
import datetime, json, os, sys, tempfile
archive, operation, rc, site = sys.argv[1:]
path = archive + '.health.json'
try:
    with open(path) as stream:
        record = json.load(stream)
except (OSError, ValueError):
    record = {}
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
record.update(schema_version=1, cluster=site, archive=archive,
              operation=operation, exit_code=int(rc), updated_at=now,
              host=os.uname().nodename, job_id=os.environ.get('SLURM_JOB_ID'))
if operation in ('save_cmd', 'incsave_cmd', 'compact_cmd'):
    if int(rc) == 0:
        record.pop('maintenance', None)
        record.update(last_success_at=now, last_success_job=os.environ.get('SLURM_JOB_ID'),
                      last_success_autosave_id=os.environ.get('HPC_SNAPSHOT_AUTOSAVE_ID'), consecutive_failures=0)
    elif not (operation == 'incsave_cmd' and int(rc) == 3):
        record['consecutive_failures'] = record.get('consecutive_failures', 0) + 1
        record['last_failure'] = dict(operation=operation, exit_code=int(rc), at=now)
    else:
        record['maintenance'] = dict(operation='compaction_required', at=now)
if int(rc) == 0 and operation in ('save_cmd', 'incsave_cmd', 'compact_cmd', 'restore_cmd', 'verify_cmd'):
    record['last_verified_at'] = now
fd, tmp = tempfile.mkstemp(prefix='.snapshot-health.', dir=os.path.dirname(path))
with os.fdopen(fd, 'w') as stream:
    json.dump(record, stream, sort_keys=True)
    stream.write('\n')
os.replace(tmp, path)
PY
}

tar_excludes() {
    printf '%s\n' \
        "--exclude=.venv" \
        "--exclude=*/.venv" \
        "--exclude=./venvs" \
        "--exclude=*/uv-bootstrap" \
        "--exclude=*/python-managed"
}

# Depth-one entries of the base, minus the caches and scratch that must never
# enter the archive, plus the one uv cache subtree that must.
write_tar_roots() {
    local base="$1"
    local output="$2"
    find "$base" \
        -xdev \
        -mindepth 1 \
        -maxdepth 1 \
        ! -name cache \
        ! -name tmp \
        -printf './%f\0' > "$output"
    local uv_relative=cache/uv
    [[ '@ADAPTER@' != psc ]] || uv_relative="cache/$USER/uv"
    if [ -d "$base/$uv_relative" ]; then
        printf './%s\0' "$uv_relative" >> "$output"
    fi
}

# Staging happens on the job-local disk so tar never streams a partial file over
# the network, and so a killed job cannot leave debris in the archive directory.
make_stage_dir() {
    local base="$1"
    local stage_base="${@PREFIX@_LOCAL_SNAPSHOT_STAGE_DIR:-$base/tmp}"
    mkdir -p "$stage_base"
    mktemp -d "$stage_base/@SITE@-local-snapshot-stage.XXXXXXXX"
}

copy_large_atomic() {
    local src="$1"
    local dst="$2"
    local tmp="${dst}.tmp.$$"
    mkdir -p "$(dirname "$dst")"
    rm -f "$tmp"
    cp -f "$src" "$tmp"
    mv -f "$tmp" "$dst"
}

verify_pack() {
    tar --listed-incremental=/dev/null --use-compress-program 'zstd -T0 -d' -tf "$1" >/dev/null
}

snapshot_budget() {
    local source="$1" destination="$2"
    if [[ '@SITE@' == msi && "$destination" == "$HOME/"* ]]; then
        local usage
        usage="$(userquota -c -U G | awk -F, -v user="$USER" '$1==user {print $2}')"
        [[ "$usage" =~ ^[0-9]+([.][0-9]+)?$ ]] || die 'home quota unknown; refusing snapshot publication'
        python3 - "$usage" "$(stat -c %s "$source")" "${@PREFIX@_LOCAL_SNAPSHOT_HOME_BUDGET_GB:-100}" <<'PY'
import sys
used, size, budget = map(float, sys.argv[1:])
assert used + size / 1e9 <= budget, 'snapshot would exceed home operating budget'
PY
    fi
}

prune_backups() {
    local archive="$1"
    local keep="${@PREFIX@_LOCAL_SNAPSHOT_BACKUP_KEEP:-1}"
    local archive_dir archive_base inc_base backups stale suffix inc_backup
    case "$keep" in
        ''|*[!0-9]*) die "@PREFIX@_LOCAL_SNAPSHOT_BACKUP_KEEP must be a non-negative integer" ;;
    esac
    archive_dir="$(dirname "$archive")"
    archive_base="$(basename "$archive")"
    inc_base="$(basename "$(incremental_dir "$archive")")"

    mapfile -t backups < <(find "$archive_dir" -maxdepth 1 -type f -name "${archive_base}.bak.*" | sort)
    while [ "${#backups[@]}" -gt "$keep" ]; do
        stale="${backups[0]}"
        suffix="${stale#"$archive_dir/$archive_base.bak."}"
        inc_backup="$archive_dir/${inc_base}.bak.${suffix}"
        rm -f "$stale"
        rm -rf "$inc_backup"
        backups=("${backups[@]:1}")
    done
}

reset_incremental_baseline() {
    local base="$1"
    local archive="$2"
    local inc_dir stage snapshot_tmp roots_file
    inc_dir="$(incremental_dir "$archive")"
    stage="$(make_stage_dir "$base")"
    snapshot_tmp="$stage/snapshot.snar"
    roots_file="$stage/roots.list"

    write_tar_roots "$base" "$roots_file"
    tar \
        --ignore-failed-read \
        --warning=no-file-changed \
        --listed-incremental="$snapshot_tmp" \
        --level=0 \
        $(tar_excludes) \
        -cf /dev/null \
        -C "$base" \
        --null \
        --files-from="$roots_file"
    mkdir -p "$inc_dir"
    copy_large_atomic "$snapshot_tmp" "$inc_dir/snapshot.snar"
    rm -rf "$stage"
}

rebaseline_cmd() {
    local base archive inc_dir
    base="$(ensure_base)" || return $?
    archive="$(archive_path "${1:-}")"
    [ -f "$archive" ] || die "full snapshot is missing: $archive"
    reset_incremental_baseline "$base" "$archive"
    inc_dir="$(incremental_dir "$archive")"
    echo "$inc_dir/snapshot.snar"
}

restore_cmd() {
    local base archive inc_dir inc stage staged digest previous_digest
    base="$(ensure_base)" || return $?
    archive="$(archive_path "${1:-}")"
    inc_dir="$(incremental_dir "$archive")"

    if [ ! -f "$archive" ]; then
        echo "No prior snapshot; initialized $base"
        return 0
    fi
    # Validate the whole chain before incremental extraction can delete files.
    # A bad late pack must not leave a partially restored workspace behind.
    echo "Verifying full snapshot: $archive" >&2
    verify_pack "$archive"
    if [ -d "$inc_dir" ]; then
        while IFS= read -r inc; do
            [ -n "$inc" ] || continue
            echo "Verifying incremental snapshot: $inc" >&2
            verify_pack "$inc"
        done < <(find "$inc_dir" -maxdepth 1 -type f -name '*.tar.zst' | sort)
    fi
    stage="$(make_stage_dir "$base")"
    staged="$stage/$(basename "$archive")"
    cp -f "$archive" "$staged"
    echo "Restoring verified full snapshot: $archive" >&2
    tar --listed-incremental=/dev/null --use-compress-program 'zstd -T0 -d' -xf "$staged" -C "$base"
    rm -f "$staged"
    if [ -d "$inc_dir" ]; then
        previous_digest=""
        while IFS= read -r inc; do
            [ -n "$inc" ] || continue
            digest="$(sha256sum "$inc")"
            digest="${digest%% *}"
            if [ "$digest" = "$previous_digest" ]; then
                echo "Skipping identical consecutive incremental: $inc" >&2
                continue
            fi
            staged="$stage/$(basename "$inc")"
            cp -f "$inc" "$staged"
            echo "Restoring verified incremental snapshot: $inc" >&2
            tar --listed-incremental=/dev/null --use-compress-program 'zstd -T0 -d' -xf "$staged" -C "$base"
            rm -f "$staged"
            previous_digest="$digest"
        done < <(find "$inc_dir" -maxdepth 1 -type f -name '*.tar.zst' | sort)
    fi
    rm -rf "$stage"
    reset_incremental_baseline "$base" "$archive"
    echo "$base"
}

save_cmd() {
    local base archive tmp backup inc_dir inc_backup snapshot_tmp stage
    local local_archive local_inc_dir roots_file
    base="$(ensure_base)" || return $?
    archive="$(archive_path "${1:-}")"
    inc_dir="$(incremental_dir "$archive")"
    backup="${archive}.bak.$(date '+%Y%m%d_%H%M%S').$$"
    inc_backup="${inc_dir}.bak.$(date '+%Y%m%d_%H%M%S').$$"
    stage="$(make_stage_dir "$base")"
    local_archive="$stage/$(basename "$archive")"
    local_inc_dir="$stage/$(basename "$inc_dir").new"
    snapshot_tmp="$local_inc_dir/snapshot.snar"
    roots_file="$stage/roots.list"

    mkdir -p "$local_inc_dir"
    write_tar_roots "$base" "$roots_file"
    tar \
        --ignore-failed-read \
        --warning=no-file-changed \
        --listed-incremental="$snapshot_tmp" \
        --level=0 \
        $(tar_excludes) \
        --use-compress-program 'zstd -T0 -3' \
        -cf "$local_archive" \
        -C "$base" \
        --null \
        --files-from="$roots_file"
    verify_pack "$local_archive"
    snapshot_budget "$local_archive" "$archive"
    tmp="${archive}.tmp.$$"
    copy_large_atomic "$local_archive" "$tmp"
    verify_pack "$tmp"
    if [ -f "$archive" ]; then
        mv "$archive" "$backup"
    fi
    mv -f "$tmp" "$archive"
    if [ -d "$inc_dir" ]; then
        mv "$inc_dir" "$inc_backup"
    fi
    rm -rf "$inc_dir"
    mkdir -p "$inc_dir"
    cp -f "$snapshot_tmp" "$inc_dir/snapshot.snar"
    rm -rf "$stage"
    prune_backups "$archive"
    echo "$archive"
}

compact_cmd() {
    save_cmd "${1:-}"
}

incsave_cmd() {
    local base archive inc_dir snapshot snapshot_tmp ts final stage
    local local_tmp network_tmp roots_file max_ratio archive_size local_size
    base="$(ensure_base)" || return $?
    archive="$(archive_path "${1:-}")"
    inc_dir="$(incremental_dir "$archive")"
    snapshot="$inc_dir/snapshot.snar"
    mkdir -p "$inc_dir"

    # No full snapshot or no baseline means there is nothing to be incremental
    # against; fall back to a full save, which also establishes the baseline.
    if [ ! -f "$archive" ] || [ ! -f "$snapshot" ]; then
        save_cmd "$archive"
        return
    fi

    stage="$(make_stage_dir "$base")"
    ts="$(date '+%Y%m%d_%H%M%S%N')"
    snapshot_tmp="$stage/snapshot.snar"
    local_tmp="$stage/incremental-${ts}.tar.zst"
    final="$inc_dir/incremental-${ts}.tar.zst"
    network_tmp="${final}.tmp.$$"
    roots_file="$stage/roots.list"

    cp -f "$snapshot" "$snapshot_tmp"
    write_tar_roots "$base" "$roots_file"
    tar \
        --ignore-failed-read \
        --warning=no-file-changed \
        --listed-incremental="$snapshot_tmp" \
        $(tar_excludes) \
        --use-compress-program 'zstd -T0 -3' \
        -cf "$local_tmp" \
        -C "$base" \
        --null \
        --files-from="$roots_file"
    verify_pack "$local_tmp"

    # A chain whose packs approach the size of the full snapshot costs more to
    # restore than it saves to write; ask for a compaction instead.
    max_ratio="${@PREFIX@_LOCAL_SNAPSHOT_MAX_INCREMENTAL_RATIO:-50}"
    case "$max_ratio" in
        ''|*[!0-9]*) die "@PREFIX@_LOCAL_SNAPSHOT_MAX_INCREMENTAL_RATIO must be a non-negative integer" ;;
    esac
    if [ "$max_ratio" -gt 0 ] && [ -f "$archive" ]; then
        archive_size="$(stat -c '%s' "$archive")"
        local_size="$(stat -c '%s' "$local_tmp")"
        if [ "$archive_size" -gt 0 ] && [ $(( local_size * 100 )) -gt $(( archive_size * max_ratio )) ]; then
            echo "@SITE@-local-snapshot: incremental too large: ${local_size} bytes > ${max_ratio}% of full archive (${archive_size} bytes); run '@SITE@-local-snapshot save' to compact" >&2
            rm -rf "$stage"
            return 3
        fi
    fi

    snapshot_budget "$local_tmp" "$final"
    copy_large_atomic "$local_tmp" "$network_tmp"
    verify_pack "$network_tmp"
    mv -f "$network_tmp" "$final"
    cp -f "$snapshot_tmp" "$snapshot"
    rm -rf "$stage"
    echo "$final"
}

autosave_cmd() {
    local interval="${1:-300}"
    local archive_arg="${2:-}"
    local compact_interval="${@PREFIX@_LOCAL_SNAPSHOT_COMPACT_SECONDS:-21600}"
    local last_compact archive_resolved pid_file

    case "$interval" in
        ''|*[!0-9]*) die "SECONDS must be a positive integer" ;;
    esac
    [ "$interval" -gt 0 ] || die "SECONDS must be greater than 0"
    case "$compact_interval" in
        ''|*[!0-9]*) die "@PREFIX@_LOCAL_SNAPSHOT_COMPACT_SECONDS must be a positive integer" ;;
    esac
    [ "$compact_interval" -gt 0 ] || die "@PREFIX@_LOCAL_SNAPSHOT_COMPACT_SECONDS must be greater than 0"

    archive_resolved="$(archive_path "$archive_arg")"
    exec 7>"${archive_resolved}.autosave.core.lock"
    flock -n 7 || die "autosave already owns this archive"
    pid_file="$(autosave_pid_path "$archive_resolved")"
    write_autosave_identity "$pid_file"
    export HPC_SNAPSHOT_AUTOSAVE_ID="$(hostname):$$:$(awk '{print $22}' /proc/$$/stat)"

    echo "@PREFIX@_LOCAL_AUTOSAVE base=$(local_base)"
    echo "archive:  $archive_resolved"
    echo "interval: ${interval}s"
    echo "compact:  ${compact_interval}s"
    echo "pid:      $$"

    # Every tick is wrapped so that one failed pack never terminates the loop.
    # Set by run_tick so the caller can react to why a tick failed.
    last_tick_status=0

    run_tick() {
        local label="$1"
        local fn="$2"
        local now status tmp_out result
        now="$(date '+%Y-%m-%d %H:%M:%S')"
        echo "[$now] autosave tick: $label"
        tmp_out="$(mktemp "${TMPDIR:-/tmp}/@SITE@-local-snapshot-autosave.XXXXXXXX")"
        set +e
        (
            set -euo pipefail
            with_lock "$archive_resolved" transaction_cmd "${fn%_cmd}" "$archive_resolved"
        ) >"$tmp_out" 2>&1
        status=$?
        set -e
        last_tick_status="$status"
        result="$(tail -n 1 "$tmp_out" 2>/dev/null || true)"
        if [ "$status" -eq 0 ]; then
            echo "[$now] $label ok: $result"
            rm -f "$tmp_out"
            return 0
        fi
        cat "$tmp_out" >&2 || true
        rm -f "$tmp_out"
        if [[ "$status" == 3 && "$fn" == incsave_cmd ]]; then
            echo "[$now] $label: compaction required; starting a full save"
        else
            echo "[$now] $label failed (status $status); autosave will retry" >&2
        fi
        return 1
    }

    stop_autosave() {
        echo "autosave: stopping, final incremental save..."
        if ! run_tick incsave incsave_cmd; then
            [[ "$last_tick_status" != 3 ]] || run_tick compact compact_cmd || true
        fi
        rm -f "$pid_file"
        exit 0
    }

    trap 'stop_autosave' INT TERM
    last_compact="$(date '+%s')"
    if ! run_tick incsave incsave_cmd; then
        [[ "$last_tick_status" != 3 ]] || run_tick compact compact_cmd || true
    fi
    while true; do
        local delay="$interval" remaining
        if [[ "${HPC_SNAPSHOT_END_EPOCH:-}" =~ ^[0-9]+$ ]]; then
            remaining=$((HPC_SNAPSHOT_END_EPOCH - $(date +%s) - ${@PREFIX@_LOCAL_SNAPSHOT_END_MARGIN:-120}))
            if [[ "$remaining" -le 0 && "${deadline_saved:-0}" == 0 ]]; then
                if run_tick before_deadline incsave_cmd; then deadline_saved=1
                elif [[ "$last_tick_status" == 3 ]] && run_tick compact compact_cmd; then deadline_saved=1; fi
            elif [[ "$remaining" -gt 0 && "$remaining" -lt "$delay" ]]; then delay="$remaining"; fi
        fi
        # A detached timer must not keep the writer lease after autosave exits.
        sleep "$delay" 7>&- &
        wait "$!" || true
        if [ $(( $(date '+%s') - last_compact )) -ge "$compact_interval" ]; then
            if run_tick compact compact_cmd; then
                last_compact="$(date '+%s')"
            fi
        elif ! run_tick incsave incsave_cmd; then
            # Status 3 is incsave reporting that the chain has outgrown its
            # budget, and the remedy it names is a compaction. Repeating the
            # same incremental every interval would fail identically until the
            # compact timer happened to fire, archiving nothing in between.
            if [ "$last_tick_status" -eq 3 ]; then
                if run_tick compact compact_cmd; then
                    last_compact="$(date '+%s')"
                fi
            fi
        fi
    done
}

start_cmd() {
    local interval="${1:-300}"
    local archive_arg="${2:-}"
    local archive pid_file log_file pid script
    archive="$(archive_path "$archive_arg")"
    pid_file="$(autosave_pid_path "$archive")"
    log_file="$(autosave_log_path "$archive")"
    script="$(readlink -f "$0")"
    if [ -f "$pid_file" ]; then
        if read_autosave_identity "$pid_file"; then
            echo "autosave already running: pid=$pid log=$log_file"
            return 0
        fi
        die "autosave identity cannot be verified on this node; inspect $pid_file"
    fi
    if command -v setsid >/dev/null 2>&1; then
        nohup setsid -f "$script" autosave "$interval" "$archive" >>"$log_file" 2>&1 </dev/null
    else
        nohup "$script" autosave "$interval" "$archive" >>"$log_file" 2>&1 </dev/null &
    fi
    for _ in $(seq 1 50); do
        if [ -f "$pid_file" ]; then
            if read_autosave_identity "$pid_file"; then
                echo "autosave started: pid=$pid log=$log_file"
                return 0
            fi
        fi
        sleep 0.1
    done
    die "autosave failed to start; see $log_file"
}

stop_cmd() {
    local archive pid_file pid
    archive="$(archive_path "${1:-}")"
    pid_file="$(autosave_pid_path "$archive")"
    [ -f "$pid_file" ] || die "autosave is not running"
    read_autosave_identity "$pid_file" || die "refusing to signal unverifiable autosave identity: $pid_file"
    if kill -0 "$pid" 2>/dev/null; then
        kill -TERM "$pid"
        for _ in $(seq 1 60); do
            kill -0 "$pid" 2>/dev/null || break
            sleep 1
        done
        if kill -0 "$pid" 2>/dev/null; then
            die "autosave did not stop within 60s; pid=$pid"
        fi
    fi
    rm -f "$pid_file"
    echo "autosave stopped"
}

log_cmd() {
    autosave_log_path "$(archive_path "${1:-}")"
}

status_cmd() {
    local base archive inc_dir pid_file log_file pid
    base="$(ensure_base)" || return $?
    archive="$(archive_path "${1:-}")"
    inc_dir="$(incremental_dir "$archive")"
    pid_file="$(autosave_pid_path "$archive")"
    log_file="$(autosave_log_path "$archive")"

    echo "local:   $base"
    du -sh "$base" 2>/dev/null || true
    echo "archive: $archive"
    if [ -f "$archive" ]; then
        ls -lh "$archive"
    else
        echo "archive: missing"
    fi
    echo "incremental_dir: $inc_dir"
    if [ -d "$inc_dir" ]; then
        find "$inc_dir" -maxdepth 1 -type f -name '*.tar.zst' | wc -l | awk '{print "incremental_packs: "$1}'
        du -sh "$inc_dir" 2>/dev/null || true
    else
        echo "incremental_dir: missing"
    fi
    echo "autosave_pid: $pid_file"
    if [ -f "$pid_file" ]; then
        if read_autosave_identity "$pid_file"; then
            echo "autosave: running pid=$pid"
        else
            echo "autosave: stale pid=$pid"
        fi
    else
        echo "autosave: stopped"
    fi
    echo "autosave_log: $log_file"
}

@GENERATION_ENGINE@

ready_cmd() {
    local archive pid_file deadline
    archive="$(archive_path "${1:-}")"
    pid_file="$(autosave_pid_path "$archive")"
    deadline=$(( $(date +%s) + ${@PREFIX@_LOCAL_SNAPSHOT_READY_SECONDS:-1800} ))
    while [[ "$(date +%s)" -lt "$deadline" ]]; do
        if [[ -f "$pid_file" ]] && read_autosave_identity "$pid_file" &&
            python3 - "$archive.health.json" "$(hostname):$pid:$(awk '{print $22}' /proc/$pid/stat)" <<'PY'
import json, os, sys
try:
    with open(sys.argv[1]) as stream: r = json.load(stream)
    assert r.get('last_success_at') and r.get('exit_code') == 0
    assert r.get('last_success_job') == os.environ.get('SLURM_JOB_ID')
    assert r.get('last_success_autosave_id') == sys.argv[2]
except (OSError, ValueError, AssertionError):
    sys.exit(1)
PY
        then echo SNAPSHOT_AUTOMATION_READY; return; fi
        sleep 1
    done
    die 'autosave did not produce a successful initial backup before READY deadline'
}

main() {
    local cmd="${1:-}"
    case "$cmd" in
        restore|rebaseline|save|incsave|compact|verify)
            shift; with_lock "$(archive_path "${1:-}")" transaction_cmd "$cmd" "${1:-}" ;;
        autosave)   shift; autosave_cmd "${1:-300}" "${2:-}" ;;
        ready)      shift; ready_cmd "${1:-}" ;;
        start)      shift; start_cmd "${1:-300}" "${2:-}" ;;
        stop)       shift; stop_cmd "${1:-}" ;;
        log)        shift; log_cmd "${1:-}" ;;
        status)
            shift
            if [[ "${1:-}" == --json ]]; then
                shift
                archive="$(archive_path "${1:-}")"
                if [[ -f "$archive.health.json" ]]; then cat "$archive.health.json";
                else printf '{"schema_version":1,"cluster":"@SITE@","phase":"unrecorded"}\n'; fi
            else status_cmd "${1:-}"; fi
            ;;
        path)       local_base ;;
        -h|--help|help|'') usage ;;
        *)          usage >&2; exit 2 ;;
    esac
}

main "$@"
