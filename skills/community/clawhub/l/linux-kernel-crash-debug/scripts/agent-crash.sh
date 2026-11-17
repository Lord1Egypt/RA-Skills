#!/bin/bash
# agent-crash.sh - An Agent-friendly CLI wrapper for the crash utility
# Designed for autonomous agents to debug linux kernels without hanging or overloading context.

set -o pipefail
export LC_ALL=C

fail() { printf "ERROR: %s\n" "$*" >&2; exit 1; }

KERNEL=""
DUMP=""
MACRO=""

function show_help {
    echo "Usage: ./agent-crash.sh -k <vmlinux> -c <vmcore> <command> [args]"
    echo ""
    echo "Commands:"
    echo "  triage                                  - Run basic sys, log, bt triage."
    echo "  flow-deadlock                           - List UN tasks and their backtraces."
    echo "  flow-oom                                - Show overall memory, top 15 memory processes & SLABs."
    echo "  flow-arm64 <vabits> <phys> <voff> <kaslr>  - ARM64 address-layout recovery overrides."
    echo "  flow-lockdown                           - UN tasks + mutex/rwsem waiter extraction."
    echo "  dis-regs <func> <pid>                   - Disassemble function and show saved stack-frame data."
    echo "  check-poison <addr>                     - Find possible poison-like data; matches are not a diagnosis."
    echo "  read-memory <hex-address> [count]       - Read 1..256 memory words from an offline dump."
    echo "  backtrace <pid>                         - Show one task's full backtrace."
    echo "  disassemble <symbol>                    - Disassemble one kernel symbol."
    exit 1
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -k|--kernel) [[ $# -ge 2 && -n "$2" ]] || fail "Missing kernel path"; KERNEL="$2"; shift ;;
        -c|--core) [[ $# -ge 2 && -n "$2" ]] || fail "Missing dump path"; DUMP="$2"; shift ;;
        -h|--help) show_help ;;
        *)
            MACRO="$1"
            shift
            MACRO_ARGS=("$@")
            break
            ;;
    esac
    shift
done

# This wrapper is offline-only. Regular-file checks reject live proc/device inputs,
# including symlinks resolved into those trees. Paths are absolute to avoid options.
[[ -n "$KERNEL" && -n "$DUMP" ]] || fail "Both -k vmlinux and -c offline vmcore are required"
[[ $EUID -ne 0 ]] || fail "Use an unprivileged account with read access to the offline files"
for input in "$KERNEL" "$DUMP"; do
    [[ -f "$input" && -r "$input" ]] || fail "Inputs must be readable regular files"
done
KERNEL=$(realpath -e -- "$KERNEL") || fail "Cannot resolve kernel path"
DUMP=$(realpath -e -- "$DUMP") || fail "Cannot resolve dump path"
for input in "$KERNEL" "$DUMP"; do
    case "$input" in /proc/*|/sys/*|/dev/*) fail "Live kernel and device inputs are forbidden" ;; esac
done
# Do not let startup files silently add GDB/shell commands or aliases.
[[ ! -e .gdbinit && ! -e "${HOME}/.gdbinit" ]] || fail "Run without local or home .gdbinit files"
CRASH_ARGS=("--no_crashrc" "-s")

# Preserve query output until its exit status is checked. Private temporary files
# avoid buffering entire logs in shell variables and are removed on every exit.
umask 077
OUTPUT_DIR=$(mktemp -d) || fail "Cannot create private query directory"
QUERY_OUT="$OUTPUT_DIR/query.out"
QUERY_ERR="$OUTPUT_DIR/query.err"
cleanup() {
    local status=$?
    rm -f -- "$QUERY_OUT" "$QUERY_ERR"
    rmdir -- "$OUTPUT_DIR"
    return "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

valid_address() { [[ "$1" =~ ^(0x)?[0-9a-fA-F]{1,16}$ ]]; }
valid_pid() { [[ "$1" =~ ^[0-9]{1,10}$ ]]; }
valid_symbol() { [[ "$1" =~ ^[a-zA-Z_][a-zA-Z0-9_.]{0,127}$ ]]; }
require_args() { [[ ${#MACRO_ARGS[@]} -eq "$1" ]] || fail "Incorrect argument count for $MACRO"; }

# Validate the complete record, including internally constructed commands. No
# shell escapes, GDB, file inclusion, pipes, redirection or write commands pass.
valid_command() {
    case "$1" in
        sys|"sys -i"|log|bt|"bt -a"|mod|"ps -m"|"ps -G"|"kmem -i"|"kmem -s"|"foreach UN bt") return 0 ;;
    esac
    [[ "$1" =~ ^bt\ -f\ [0-9]{1,10}$ ]] && return 0
    [[ "$1" =~ ^dis\ [a-zA-Z_][a-zA-Z0-9_.]{0,127}$ ]] && return 0
    if [[ "$1" =~ ^rd\ (0x)?[0-9a-fA-F]{1,16}\ ([0-9]{1,3})$ ]]; then
        [[ ${BASH_REMATCH[2]} -ge 1 && ${BASH_REMATCH[2]} -le 256 ]] && return 0
    fi
    return 1
}

run_crash() {
    local cmd="$1" status
    valid_command "$cmd" || fail "Command outside the offline read-only allowlist"
    printf '%s\n' 'set scroll off' "$cmd" quit |
        timeout 30s crash "${CRASH_ARGS[@]}" "$KERNEL" "$DUMP" | sed '/^crash> /d'
    status=$?
    return "$status"
}

# Consume the complete stream so a display limit cannot SIGPIPE the query.
# Keep only the first/last 200 lines in memory, with bounded displayed line length.
bounded_output() {
    awk '
        {
            line = length($0) > 2048 ? substr($0, 1, 2048) " [line shortened]" : $0
            if (NR <= 200) first[NR] = line
            last[NR % 200] = line
        }
        END {
            for (i = 1; i <= NR && i <= 200; i++) print first[i]
            if (NR > 400)
                printf "[WARNING: Output truncated (%d lines; showing first/last 200).]\n", NR
            start = NR > 400 ? NR - 199 : 201
            for (i = start; i <= NR; i++) print last[i % 200]
        }'
}

query() {
    local cmd="$1" status
    run_crash "$cmd" >"$QUERY_OUT" 2>"$QUERY_ERR"
    status=$?
    if [[ $status -ne 0 ]]; then
        bounded_output <"$QUERY_OUT"
        bounded_output <"$QUERY_ERR" >&2
        printf 'ERROR: crash query failed (exit %s): %s\n' "$status" "$cmd" >&2
        exit "$status"
    fi
    bounded_output <"$QUERY_ERR" >&2
}

run_and_truncate() {
    query "$1"
    bounded_output <"$QUERY_OUT"
}

show_un_tasks() {
    query "ps -m"
    awk '/ UN / { print; found = 1 }
         END { if (!found) print "No UN task rows in the successful query." }' "$QUERY_OUT" |
        bounded_output
}

case "$MACRO" in
    triage)
        require_args 0
        echo "=== [TRIAGE: SYSTEM INFO] ==="
        run_and_truncate "sys"
        echo "=== [TRIAGE: HIGH-SIGNAL EVENT INDEX] ==="
        query "log"
        awk 'tolower($0) ~ /bug:|oops:|panic|kasan:|kfence:|kcsan:|lockdep|soft lockup|hard lockup|hung task|out of memory|oom-kill|machine check|mce:|serror|watchdog/ {
                 if (++matches <= 120) print
             }
             END { if (!matches) print "No matching events in the successful log query." }' "$QUERY_OUT" |
            bounded_output
        echo "=== [TRIAGE: KERNEL LOG (Last 100 lines)] ==="
        tail -n 100 "$QUERY_OUT" | bounded_output
        echo "=== [TRIAGE: PANIC BACKTRACE] ==="
        run_and_truncate "bt"
        echo "=== [TRIAGE: ACTIVE CPU BACKTRACES] ==="
        run_and_truncate "bt -a"
        echo "=== [TRIAGE: LOADED MODULES] ==="
        run_and_truncate "mod"
        ;;
    flow-deadlock)
        require_args 0
        echo "=== [DEADLOCK: UNINTERRUPTIBLE TASKS] ==="
        show_un_tasks
        echo "=== [DEADLOCK: WAITING TASKS BACKTRACES] ==="
        run_and_truncate "foreach UN bt"
        ;;
    flow-oom)
        require_args 0
        echo "=== [OOM: MEMORY OVERVIEW] ==="
        query "kmem -i"
        awk 'NR <= 30' "$QUERY_OUT" | bounded_output
        echo "=== [OOM: TOP 15 THREAD-GROUP LEADERS BY RSS (KiB)] ==="
        query "ps -G"
        echo "PID PPID CPU TASK ST %MEM VSZ RSS COMM"
        # A leading > marks the active task and is not a data column.
        awk '{ sub(/^[[:space:]]*>[[:space:]]*/, "") }
             $1 ~ /^[0-9]+$/ && $7 ~ /^[0-9]+$/ && $8 ~ /^[0-9]+$/ {
                 printf "%s\t%s\n", $8, $0
             }' "$QUERY_OUT" |
            sort -n -r -k 1,1 |
            awk 'NR <= 15 { sub(/^[^\t]*\t/, ""); print }' | bounded_output
        echo "=== [OOM: TOP 15 SLAB CACHES BY ALLOCATED OBJECT BYTES] ==="
        echo "Object bytes = OBJSIZE * ALLOCATED; excludes slab overhead and free capacity."
        query "kmem -s"
        echo "OBJECT_BYTES CACHE OBJSIZE ALLOCATED TOTAL SLABS SSIZE NAME"
        awk '$1 ~ /^(0x)?[0-9a-fA-F]+$/ && $2 ~ /^[0-9]+$/ && $3 ~ /^[0-9]+$/ {
                 printf "%.0f\t%s\n", $2 * $3, $0
             }' "$QUERY_OUT" |
            sort -n -r -k 1,1 |
            awk 'NR <= 15' | bounded_output
        ;;
    flow-arm64)
        require_args 4
        # ARM64-specific macro: injects -m parameters for crash
        # Usage: flow-arm64 <vabits_actual> <phys_offset> <kimage_voffset> <kaslr>
        # Example: flow-arm64 39 0x80000000 0xffffffc000000000 0x0
        VABITS="${MACRO_ARGS[0]}"
        PHYS_OFF="${MACRO_ARGS[1]}"
        KIMAGE_VOFF="${MACRO_ARGS[2]}"
        KASLR_VAL="${MACRO_ARGS[3]}"
        [[ "$VABITS" =~ ^(39|42|48|52)$ ]] || fail "Unsupported ARM64 VA bits"
        for value in "$PHYS_OFF" "$KIMAGE_VOFF" "$KASLR_VAL"; do
            valid_address "$value" || fail "ARM64 offsets must be hexadecimal values"
        done
        echo "=== [ARM64: VERIFY CRASH CAN LOAD WITH -m PARAMS] ==="
        echo "  vabits_actual=$VABITS"
        echo "  phys_offset=$PHYS_OFF"
        echo "  kimage_voffset=$KIMAGE_VOFF"
        echo "  kaslr=$KASLR_VAL"
        echo ""
        CRASH_ARGS+=("-m" "vabits_actual=$VABITS" "-m" "phys_offset=$PHYS_OFF" "-m" "kimage_voffset=$KIMAGE_VOFF" "--kaslr=0x${KASLR_VAL#0x}")
        run_and_truncate "sys"
        query "log"
        tail -n 50 "$QUERY_OUT" | bounded_output
        run_and_truncate "bt"
        echo ""
        echo "=== [AGENT HINT] ==="
        echo "These derived address overrides apply only to this invocation."
        echo "Normal distro vmcores should use triage without address overrides."
        ;;
    flow-lockdown)
        require_args 0
        # Lock contention analysis: extract UN tasks, then for each try to derive lock address
        echo "=== [LOCKDOWN: UN TASKS] ==="
        show_un_tasks
        echo ""
        echo "=== [LOCKDOWN: UN TASKS BACKTRACES] ==="
        run_and_truncate "foreach UN bt"
        echo ""
        echo "=== [LOCKDOWN: LOCK-RELATED FRAMES (first 20)] ==="
        awk '/mutex|rwsem|down_write|down_read|spin_lock|rwsem_down/ {
                 if (++matches <= 20) print
             }
             END { if (!matches) print "No matching lock-wait frames in the successful query." }' "$QUERY_OUT" |
            bounded_output
        echo ""
        echo "=== [AGENT HINT: LOCK DERIVATION TECHNIQUE] ==="
        echo "For ARM64 tasks blocked on rwsem/mutex, recover the lock argument from matching disassembly and saved state."
        echo "See references/case-studies.md Case 11 for the manual derivation."
        echo "Use wrapper disassembly and bounded reads on proven saved slots; hand unsupported type/layout queries to a human offline."
        ;;
    dis-regs)
        require_args 2
        FUNC="${MACRO_ARGS[0]}"
        PID="${MACRO_ARGS[1]}"
        valid_symbol "$FUNC" || fail "Invalid kernel symbol"
        valid_pid "$PID" || fail "Invalid PID"
        echo "=== [EXPERT: STACK-FRAME DATA FOR PID $PID] ==="
        run_and_truncate "bt -f $PID"
        echo "=== [EXPERT: DISASSEMBLY FOR $FUNC] ==="
        run_and_truncate "dis $FUNC"
        ;;
    check-poison)
        require_args 1
        ADDR="${MACRO_ARGS[0]}"
        valid_address "$ADDR" || fail "Invalid hexadecimal address"
        echo "=== [POISON CHECK: MEMORY DUMP NEAR $ADDR] ==="
        query "rd $ADDR 64"
        bounded_output <"$QUERY_OUT"
        echo "=== [POISON CHECK: POSSIBLE POISON-LIKE DATA WORDS] ==="
        # Match complete data words, never the address column or ASCII rendering.
        # A matching value is a clue; verify allocator settings and object history.
        awk '$1 ~ /^[0-9a-fA-F]+:$/ {
                 width = length($2)
                 if (width != 8 && width != 16) next
                 # Default rd displays up to 16 bytes per row, then ASCII.
                 for (i = 2; i <= NF && i <= 1 + 32 / width; i++) {
                     word = tolower($i)
                     if (word !~ /^[0-9a-f]+$/ || length(word) != width) break
                     if (word ~ /^(6b6b6b6b|6b6b6b6b6b6b6b6b|5a5a5a5a|5a5a5a5a5a5a5a5a)$/) {
                         print $1, word, "(candidate only; verify allocator and lifetime evidence)"
                         found = 1
                     }
                 }
             }
             END { if (!found) print "No repeated poison-byte data words found; corruption is not excluded." }' "$QUERY_OUT" |
            bounded_output
        ;;
    read-memory)
        [[ ${#MACRO_ARGS[@]} -ge 1 && ${#MACRO_ARGS[@]} -le 2 ]] || fail "Expected address and optional count"
        ADDR="${MACRO_ARGS[0]}"
        COUNT="${MACRO_ARGS[1]:-1}"
        valid_address "$ADDR" || fail "Invalid hexadecimal address"
        [[ "$COUNT" =~ ^[1-9][0-9]{0,2}$ && "$COUNT" -le 256 ]] || fail "Count must be 1..256"
        run_and_truncate "rd $ADDR $COUNT"
        ;;
    backtrace)
        require_args 1
        valid_pid "${MACRO_ARGS[0]}" || fail "Invalid PID"
        run_and_truncate "bt -f ${MACRO_ARGS[0]}"
        ;;
    disassemble)
        require_args 1
        valid_symbol "${MACRO_ARGS[0]}" || fail "Invalid kernel symbol"
        run_and_truncate "dis ${MACRO_ARGS[0]}"
        ;;
    *)
        echo "Unknown macro: $MACRO"
        show_help
        ;;
esac
