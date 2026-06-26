#!/bin/bash
# agent-crash.sh - An Agent-friendly CLI wrapper for the crash utility
# Designed for autonomous agents to debug linux kernels without hanging or overloading context.

KERNEL=""
DUMP=""
MACRO=""

function show_help {
    echo "Usage: ./agent-crash.sh -k <vmlinux> [-c <vmcore>] <command> [args]"
    echo ""
    echo "Commands:"
    echo "  triage                                  - Run basic sys, log, bt triage."
    echo "  flow-deadlock                           - List UN tasks and their backtraces."
    echo "  flow-oom                                - Show overall memory, top 15 memory processes & SLABs."
    echo "  flow-arm64 <vabits> <phys> <voff> <kaslr>  - ARM64 crash with -m params injected."
    echo "  flow-lockdown                           - UN tasks + mutex/rwsem waiter extraction."
    echo "  dis-regs <func> <pid>                   - Disassemble function and show stack registers side-by-side."
    echo "  check-poison <addr>                     - Check memory near address for kernel poison patterns."
    echo "  run \"<cmd>\"                             - Run arbitrary crash command with safety wrappers."
    exit 1
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -k|--kernel) KERNEL="$2"; shift ;;
        -c|--core) DUMP="$2"; shift ;;
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

if [[ -z "$KERNEL" ]]; then
    echo "ERROR: -k / --kernel must be specified."
    show_help
fi

CRASH_ARGS=("-s" "$KERNEL")
if [[ -n "$DUMP" ]]; then
    CRASH_ARGS+=("$DUMP")
fi

# Function to run crash cleanly, silently, and with a timeout
run_crash() {
    local cmd="$1"
    # Execute batch via stdin, timeout ensures agent isn't blocked forever
    echo -e "set scroll off\n${cmd}\nquit" | timeout 30s crash "${CRASH_ARGS[@]}" 2>/dev/null | grep -v "^crash> "
}

# Wrapper for truncating massive outputs that would crash the LLM
run_and_truncate() {
    local cmd="$1"
    local max_lines=400
    local output=$(run_crash "$cmd")
    local lines=$(echo "$output" | wc -l)

    if [ "$lines" -gt "$max_lines" ]; then
        echo "$output" | head -n 200
        echo ""
        echo "=========================================================================="
        echo "[WARNING: Output truncated ($lines lines total > $max_lines limit).]"
        echo "[AGENT INSTRUCTION: Use tighter crash queries if needed.]"
        echo "=========================================================================="
        echo ""
        echo "$output" | tail -n 200
    else
        echo "$output"
    fi
}

case "$MACRO" in
    triage)
        echo "=== [TRIAGE: SYSTEM INFO] ==="
        run_crash "sys"
        echo "=== [TRIAGE: KERNEL LOG (Last 100 lines)] ==="
        run_crash "log" | tail -n 100
        echo "=== [TRIAGE: PANIC BACKTRACE] ==="
        run_crash "bt"
        ;;
    flow-deadlock)
        echo "=== [DEADLOCK: UNINTERRUPTIBLE TASKS] ==="
        run_crash "ps -m" | grep " UN "
        echo "=== [DEADLOCK: WAITING TASKS BACKTRACES] ==="
        run_and_truncate "foreach UN bt"
        ;;
    flow-oom)
        echo "=== [OOM: MEMORY OVERVIEW] ==="
        run_crash "kmem -i" | head -n 30
        echo "=== [OOM: TOP 15 MEMORY HOG PROCESSES (VSZ/RSS)] ==="
        # Run ps -G, skip header, sort by memory column (usually 5th or 6th, sort by numbers backward), show top 15
        run_crash "ps -G" | sort -n -r -k 5 | head -n 15
        echo "=== [OOM: TOP 15 SLAB CACHES ALLOCATED] ==="
        run_crash "kmem -s" | sort -n -r -k 4 | head -n 15
        ;;
    flow-arm64)
        # ARM64-specific macro: injects -m parameters for crash
        # Usage: flow-arm64 <vabits_actual> <phys_offset> <kimage_voffset> <kaslr>
        # Example: flow-arm64 39 0x80000000 0xffffffc000000000 0x0
        VABITS="${MACRO_ARGS[0]}"
        PHYS_OFF="${MACRO_ARGS[1]}"
        KIMAGE_VOFF="${MACRO_ARGS[2]}"
        KASLR_VAL="${MACRO_ARGS[3]}"
        if [[ -z "$VABITS" || -z "$PHYS_OFF" || -z "$KIMAGE_VOFF" || -z "$KASLR_VAL" ]]; then
            echo "ERROR: flow-arm64 requires <vabits_actual> <phys_offset> <kimage_voffset> <kaslr>"
            echo "Example: flow-arm64 39 0x80000000 0xffffffc000000000 0x0"
            exit 1
        fi
        echo "=== [ARM64: VERIFY CRASH CAN LOAD WITH -m PARAMS] ==="
        echo "  vabits_actual=$VABITS"
        echo "  phys_offset=$PHYS_OFF"
        echo "  kimage_voffset=$KIMAGE_VOFF"
        echo "  kaslr=$KASLR_VAL"
        echo ""
        # Re-run crash with -m parameters
        ARM64_ARGS=("-s" "$KERNEL" "-m" "vabits_actual=$VABITS" "-m" "phys_offset=$PHYS_OFF" "-m" "kimage_voffset=$KIMAGE_VOFF" "-m" "kaslr=$KASLR_VAL")
        if [[ -n "$DUMP" ]]; then
            ARM64_ARGS+=("$DUMP")
        fi
        echo "=== [ARM64: TRIAGE WITH -m PARAMS] ==="
        echo -e "set scroll off\nsys\nlog | tail -50\nbt\nquit" | timeout 30s crash "${ARM64_ARGS[@]}" 2>/dev/null | grep -v "^crash> "
        echo ""
        echo "=== [ARM64: VMCOREINFO SANITY] ==="
        echo -e "set scroll off\nsys -i | head -20\nquit" | timeout 30s crash "${ARM64_ARGS[@]}" 2>/dev/null | grep -v "^crash> "
        echo ""
        echo "=== [AGENT HINT] ==="
        echo "If loading succeeds, use the wrapper as: $0 -k $KERNEL -c $DUMP \\"
        echo "  run \"bt -f <pid>\""
        echo "For per-command -m params, use: crash ${ARM64_ARGS[*]} vmlinux vmcore"
        ;;
    flow-lockdown)
        # Lock contention analysis: extract UN tasks, then for each try to derive lock address
        echo "=== [LOCKDOWN: UN TASKS] ==="
        run_crash "ps -m" | grep " UN "
        echo ""
        echo "=== [LOCKDOWN: UN TASKS BACKTRACES] ==="
        run_and_truncate "foreach UN bt"
        echo ""
        echo "=== [LOCKDOWN: MUTEX/RWSEM WAITERS (top 10)] ==="
        run_crash "foreach UN bt" | grep -E "mutex|rwsem|down_write|down_read|spin_lock|rwsem_down" | head -20
        echo ""
        echo "=== [AGENT HINT: LOCK DERIVATION TECHNIQUE] ==="
        echo "For ARM64 tasks blocked on rwsem/mutex, the lock address is in a callee-saved register."
        echo "See references/case-studies.md Case 11 for the manual derivation."
        echo "Pattern: 1) bt to get FP, 2) dis -xl to find reg save offset, 3) rd to read saved value."
        ;;
    dis-regs)
        FUNC="${MACRO_ARGS[0]}"
        PID="${MACRO_ARGS[1]}"
        if [[ -z "$FUNC" || -z "$PID" ]]; then
            echo "ERROR: dis-regs requires <func> and <pid>."
            exit 1
        fi
        echo "=== [EXPERT: REGISTERS FOR PID $PID] ==="
        run_and_truncate "bt -f $PID"
        echo "=== [EXPERT: DISASSEMBLY FOR $FUNC] ==="
        run_and_truncate "dis $FUNC"
        ;;
    check-poison)
        ADDR="${MACRO_ARGS[0]}"
        if [[ -z "$ADDR" ]]; then
            echo "ERROR: check-poison requires <addr>."
            exit 1
        fi
        echo "=== [POISON CHECK: MEMORY DUMP NEAR $ADDR] ==="
        out=$(run_crash "rd $ADDR 64")
        echo "$out"
        echo "=== [POISON CHECK: MAGIC NUMBER MATCHES] ==="
        # Grep for standard poison values:
        # 6b6b6b6b (UAF), 5a5a5a5a (SLUB uninitialized), deadbeef, 0x100/0x200 (LIST_POISON)
        echo "$out" | grep -E -i '6b6b6b6b|5a5a5a5a|deadbeef|0+100\b|0+200\b|abcd' || echo "No obvious poison match found. Agent should inspect payload manually."
        ;;
    run)
        CMD="${MACRO_ARGS[*]}"
        run_and_truncate "$CMD"
        ;;
    *)
        echo "Unknown macro: $MACRO"
        show_help
        ;;
esac
