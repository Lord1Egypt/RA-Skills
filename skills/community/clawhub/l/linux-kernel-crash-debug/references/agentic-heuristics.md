# Agentic Debugging Heuristics

This file outlines the definitive workflow an autonomous AI Agent must follow when handling advanced Linux kernel crashes using this system. It uses restricted offline analysis operations rather than arbitrary interpreter input.

## 1. Safety Directives & the `scripts/agent-crash.sh` Wrapper
Interactive commands (like a plain `crash` session REPL) will cause the Agent's subshell to freeze and timeout. Massive output (e.g., listing 100,000 active processes) will crash the Agent's context window.

**Mandate:** Always use the provided `scripts/agent-crash.sh` wrapper script instead of calling `crash` directly.
```bash
# General Syntax
./scripts/agent-crash.sh -k /path/to/vmlinux -c /path/to/vmcore <macro_or_command>

# Example: bounded offline memory read
./scripts/agent-crash.sh -k vmlinux -c vmcore read-memory ffff880123456789 128
```

Before interpreting output, follow `evidence-first-workflow.md`: record dump
completeness, kernel/module build provenance, taint, and the earliest anomaly.
The wrapper limits output volume; it does not make mismatched symbols or a
filtered-out address trustworthy.

Nonzero crash/timeout process statuses are propagated with bounded diagnostics.
A zero exit status alone does not prove command-level success: inspect errors
and warnings, and keep unreadable or missing evidence unknown.

## 2. Upstream Verification (The Hacker Instinct)
Before diving into assembly, a seasoned kernel developer checks for known fixes.
- If `scripts/agent-crash.sh -k vmlinux -c vmcore triage` reveals a `kernel BUG at fs/pipe.c:120!`, the Agent should parse the signature and first sanitize the signature (remove hostnames, customer identifiers, paths, addresses, credentials, and proprietary modules), then search official upstream sources or use local `git grep` on the Linux kernel to see if this has already been fixed. A matching report is a candidate; compare the affected code and build before applying its conclusion.

## 3. High-Level Macro Workflows (1:1 Case Mapping)

The wrapper provides tailored APIs for standard debugging methodologies defined in `case-studies.md`.

* **Triage / Base Panic**: `scripts/agent-crash.sh -k vmlinux -c vmcore triage`
  Provides `sys`, a high-signal event index, log tail, panic/all-CPU backtraces,
  and the loaded-module inventory.
* **Deadlock Analysis**: `scripts/agent-crash.sh -k vmlinux -c vmcore flow-deadlock`
  Automatically extracts all UN (Uninterruptible) task backtraces filtering out idle CPU noise.
* **OOM Analysis**: `scripts/agent-crash.sh -k vmlinux -c vmcore flow-oom`
  Ranks thread-group leaders by RSS and slab caches by `OBJSIZE * ALLOCATED`.
  RSS includes shared pages, while allocated object bytes exclude free slab
  capacity and allocator overhead; these rankings are not a complete memory
  accounting or proof of a leak.

## 4. The "Linus" Method: Reverse Engineering 
If line numbers from Backtraces are wrong due to compiler optimization (`-O2`):
- **Command**: `scripts/agent-crash.sh -k vmlinux -c vmcore dis-regs <faulty_function> <panicked_pid>`
- **Technique**: Match the faulting PC/instruction to the analyzed build. `bt -f`
  displays stack-frame data; it does not guarantee fault-context values for
  arbitrary registers or tasks. Use saved exception registers from the Oops or
  a verified exception frame when available, and recover other values only
  where the disassembly and saved state support them. Keep unavailable values
  unknown. Reconstruct the effective address before identifying the affected
  object; the dereference site may be a victim of earlier corruption.

## 5. Memory Poison Dictionary Validation
When inspecting a corrupted pointer or structure:
- **Command**: `scripts/agent-crash.sh -k vmlinux -c vmcore check-poison <suspicious_address>`
- **Interpretation**: The wrapper flags complete data words containing repeated
  `0x6b` (`POISON_FREE`) or `0x5a` (`POISON_INUSE`) as candidates only. Confirm the
  target allocator's poisoning configuration, object bounds, allocation state,
  and alloc/free history before claiming UAF or an uninitialized access. A
  matching constant may be ordinary payload; no match does not exclude damage.
- **List pointers**: Inspect the analyzed kernel's `LIST_POISON1`,
  `LIST_POISON2`, and `POISON_POINTER_DELTA` definitions. Numeric offsets vary
  by kernel version and may be relocated by `CONFIG_ILLEGAL_POINTER_VALUE`;
  small values such as `0x100` or `0x200` are not universal signatures. The
  wrapper does not infer list deletion or object lifetime from these values.
  See [Linux poison definitions](https://github.com/torvalds/linux/blob/v6.12/include/linux/poison.h)
  and [crash bt help](https://crash-utility.github.io/help_pages/bt.html).

## 6. Fallback Strategy
If high-level macros leave an evidence gap, use only the wrapper's restricted primitives:
- `./scripts/agent-crash.sh -k vmlinux -c vmcore read-memory <hex-address> <count>` (1..256 words).
- `./scripts/agent-crash.sh -k vmlinux -c vmcore backtrace <numeric-pid>`.
- `./scripts/agent-crash.sh -k vmlinux -c vmcore disassemble <kernel-symbol>`.

The unrestricted `run` operation is removed. Do not bypass this boundary with direct crash/GDB input, shell escapes, command files, or extensions. For an unsupported operation such as structure-list traversal, document the missing evidence and hand the exact offline query to an authorized human. Both files must be readable regular files; use an unprivileged account without local/home `.gdbinit`. Keep dumps and output protected. Timeout/truncation are resource limits, not an OS sandbox.

## 7. Required Conclusion Format

An agent conclusion must distinguish:

1. the **fault/detection site**;
2. the suspected **corruption or stall origin**;
3. the defensible **root cause**;
4. missing evidence and dump/filter limitations;
5. a competing hypothesis and its disproof test;
6. confidence (`high`, `medium`, or `low`).

If only the first item is known, report a localization result rather than a
root cause. Never turn an unresolved pointer value or an unavailable page into
a confident causal claim.
