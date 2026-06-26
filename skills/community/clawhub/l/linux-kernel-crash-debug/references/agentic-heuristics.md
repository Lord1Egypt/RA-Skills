# Agentic Debugging Heuristics

This file outlines the definitive workflow an autonomous AI Agent must follow when handling advanced Linux kernel crashes using this system. It replaces raw human CLI execution with "Agent-Safe" API methodologies.

## 1. Safety Directives & the `scripts/agent-crash.sh` Wrapper
Interactive commands (like a plain `crash` session REPL) will cause the Agent's subshell to freeze and timeout. Massive output (e.g., listing 100,000 active processes) will crash the Agent's context window.

**Mandate:** Always use the provided `scripts/agent-crash.sh` wrapper script instead of calling `crash` directly.
```bash
# General Syntax
./scripts/agent-crash.sh -k /path/to/vmlinux -c /path/to/vmcore <macro_or_command>

# Example: Fallback raw command execution (Safe, truncated, non-blocking)
./scripts/agent-crash.sh -k vmlinux -c vmcore run "rd ffff880123456789 128"
```

## 2. Upstream Verification (The Hacker Instinct)
Before diving into assembly, a seasoned kernel developer checks for known fixes.
- If `scripts/agent-crash.sh triage` reveals a `kernel BUG at fs/pipe.c:120!`, the Agent should parse the signature and perform a quick web search or `git grep` on the upstream Linux kernel to see if this has already been fixed. Do not reinvent the wheel if a known CVE/Bugzilla is present.

## 3. High-Level Macro Workflows (1:1 Case Mapping)

The wrapper provides tailored APIs for standard debugging methodologies defined in `case-studies.md`.

* **Triage / Base Panic**: `scripts/agent-crash.sh -k vmlinux triage`
  Provides a clean `sys` environment, tail of the log, and crash backtrace.
* **Deadlock Analysis**: `scripts/agent-crash.sh -k vmlinux flow-deadlock`
  Automatically extracts all UN (Uninterruptible) task backtraces filtering out idle CPU noise.
* **OOM Analysis**: `scripts/agent-crash.sh -k vmlinux flow-oom`
  Automatically runs complex sorts to deliver the explicitly top 15 memory-hogging processes and SLAB caches without overflowing the Agent's context.

## 4. The "Linus" Method: Reverse Engineering 
If line numbers from Backtraces are wrong due to compiler optimization (`-O2`):
- **Command**: `scripts/agent-crash.sh -k vmlinux dis-regs <faulty_function> <panicked_pid>`
- **Technique**: Read the exact `dis` assembly pointer (RIP). Cross-reference the exact active `%rax`, `%rdi`, or `%rsi` registers returned by `bt -f`. Map the assembly instructions to the C source snippet to deduce exactly what variable caused the corruption or NULL deref.

## 5. Memory Poison Dictionary Validation
When inspecting a corrupted pointer or structure:
- **Command**: `scripts/agent-crash.sh -k vmlinux check-poison <suspicious_address>`
- **Logic**: The Agent should instantly flag the bug if the script detects these magic values:
  - `0x6b6b6b6b`: Use After Free (`POISON_FREE`)
  - `0x5a5a5a5a`: Uninitialized SLUB Object (`POISON_INUSE`)
  - `0x0000000000000100` (`LIST_POISON1`): Traversing a deleted list `next`
  - `0x0000000000000200` (`LIST_POISON2`): Traversing a deleted list `prev`

## 6. Fallback Strategy
If all high-level macros fail to pinpoint the kernel anomaly, the Agent **must fall back to manual raw commands**.
- Use `./scripts/agent-crash.sh -k vmlinux run "<command>"` for primitives.
- Use `rd <addr> <count>` for manual stack unwinding if `bt` is broken (Double Fauts).
- Use `list -h <start>` to manually walk broken structures.
- Remember the output is truncated to 400 lines by the wrapper for your safety. Do not request massively broad sweeps.
