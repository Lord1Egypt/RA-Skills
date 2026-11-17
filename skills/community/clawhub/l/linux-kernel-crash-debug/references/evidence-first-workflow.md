# Evidence-First Kernel Crash Workflow

> Language note: Chinese explanations and original source titles are optional companion material. Follow the user’s preferred language and translate relevant passages when needed; no locale is required.


This workflow turns a panic log or vmcore into a testable root-cause report. It
is intentionally stricter than a command cheat sheet: every conclusion must be
linked to preserved evidence, and every hypothesis must have a disproof test.

## Contents

1. Analysis contract and evidence hierarchy
2. Dump/symbol validation
3. Failure timeline reconstruction
4. Crash-class routing and tool escalation
5. Hypothesis testing and confidence
6. Known-fix/regression verification
7. Root-cause report template and primary sources

## 1. Analysis Contract

Before investigating, record these facts. If a fact is unknown, keep it marked
as unknown instead of guessing.

| Field | Why it matters |
|---|---|
| Kernel release and full build string | Same release text can still refer to a different build |
| Architecture and platform | Register conventions, exception frames, and address translation differ |
| `vmlinux` path and GNU build ID | Establishes symbol provenance |
| vmcore path, size, checksum, and format | Detects truncation, replacement, and unsupported formats |
| Matching module `.ko` files and build IDs | An unloaded or out-of-tree module may contain the faulting instruction |
| Kernel command line and `.config` | Explains KASLR, sanitizers, watchdogs, preemption, and dump behavior |
| Taint flags | Identifies proprietary/out-of-tree modules, prior warnings, machine checks, and live patching |
| First observable anomaly | Later panics are often secondary damage |
| Reproduction trigger and last known-good version | Separates deterministic bugs from regressions and hardware faults |

Preserve raw artifacts before conversion or filtering:

```bash
sha256sum vmcore vmlinux > evidence.sha256
file vmcore vmlinux
readelf -n vmlinux | grep -F 'Build ID'
makedumpfile --dump-dmesg vmcore vmcore-dmesg.txt
```

Do not overwrite the original dump with a converted or filtered copy. Record
the `makedumpfile` filter level because excluded user, cache, or free pages can
make later memory queries inconclusive.

## 2. Evidence Hierarchy

Use the strongest available source first:

1. **vmcore + exact debuginfo + matching modules**: best for stateful,
   post-mortem analysis.
2. **Complete Oops/panic log**: often enough to locate the fault and classify
   the exception, but not to inspect arbitrary state.
3. **pstore/ramoops, serial console, netconsole, or BMC console**: vital when
   kdump never ran or the machine reset immediately.
4. **Watchdog, MCE/APEI/EDAC, and firmware records**: may be the only evidence
   for hard lockups and hardware-originated failures.
5. **Symptoms without a stack or timestamped log**: insufficient for a root
   cause. Improve capture before making a strong claim.

`vmcore-dmesg.txt` is worth collecting even when the full vmcore is incomplete:
the kernel ring buffer is normally written first and often retains the primary
failure signature.

## 3. Phase A — Validate Before Interpreting

### 3.1 Start with bounded triage

Agents must use the non-interactive wrapper:

```bash
./scripts/agent-crash.sh -k /path/to/vmlinux -c /path/to/vmcore triage
```

Human interactive equivalent:

```console
crash> sys
crash> log
crash> bt
crash> bt -a
crash> mod
```

Reject or downgrade the analysis if any of these checks fail:

- `sys` release/build does not match the supplied kernel artifacts.
- Symbols resolve to implausible functions or source lines.
- The faulting address belongs to a module whose matching `.ko` is absent.
- The dump is marked partial and the required address was filtered out.
- The log contains evidence of an earlier Oops, warning, MCE, or allocator
  corruption that precedes the final panic.

Load matching module symbols when required:

```console
crash> mod
crash> mod -s <module_name> /path/to/module.ko
```

### 3.2 Treat ARM64 `-m` parameters as a fallback

Modern kdump vmcores normally carry address-layout data in VMCOREINFO, which is
consumed by `crash` and `makedumpfile`. Try the standard invocation first:

```bash
crash vmlinux vmcore
```

Only derive `vabits_actual`, `phys_offset`, `kimage_voffset`, and `kaslr` when
the dump is raw RAM, VMCOREINFO is missing/damaged, or `crash` explicitly fails
address translation. See `arm64-crash-params.md` for that recovery path. Never
copy parameter values from another boot.

## 4. Phase B — Reconstruct the Failure Timeline

Read the log chronologically, not just its last screen. Build a short timeline:

```text
T-?     first warning / allocator report / MCE / hung-task report
T-Δ     workload or device event
T0      first Oops, BUG, lockup, or panic
T+Δ     secondary faults, recursive panic, kdump transition
```

Ask four questions:

1. What is the earliest abnormal event?
2. Which CPU/task first reported it?
3. Was the final panic deliberate (`panic_on_warn`, watchdog panic, SysRq-c,
   OOM panic) or caused by an unrecoverable exception?
4. Did another CPU or subsystem already report corruption?

The panic task is not automatically the culprit. It may be the first task to
touch memory corrupted earlier, the watchdog that noticed a stalled CPU, or the
OOM killer reacting to a long-running leak.

For an NMI or hardware-error report, separate the handler's stack from the
interrupted context. A frame such as `intel_idle` tells you where the CPU was
interrupted; it does not by itself identify a faulty driver. Correlate the
notification path, syndrome, and timestamped firmware/BMC/PCIe records before
attributing the failure. See the [hardware-panic investigation](https://blog.alicegoldfuss.com/debugging-hardware-panic/)
for this evidence handoff; its hardware replacement request is not a documented
long-term verification result.

## 5. Phase C — Classify and Route

| Signature | First checks | Preferred next tool |
|---|---|---|
| NULL/near-NULL fault | Fault address, instruction operands, object lifetime | `bt -f`, `dis`, structure offsets |
| Wild pointer / poison value | Alloc/free history, slab cache, neighboring objects | KASAN, KFENCE, SLUB debug, page_owner |
| Suspected single-bit pointer corruption | Effective address, XOR difference, same-boot layout, object semantics | [Candidate validation (§5.1.1)](#511-arm64-single-bit-pointer-corruption-hypotheses) and Case 16 |
| OOM / allocation failure | OOM log, zones, slabs, task RSS, fragmentation | `flow-oom`, `kmem`, page_owner |
| Soft lockup | Stuck CPU stack, scheduler progress, lock owner | `bt -a`, SysRq-l, ftrace |
| Hard lockup | NMI stack, interrupt state, firmware/BMC evidence | NMI watchdog, pstore, hardware logs |
| Hung task | All `UN` tasks, wait channel, completion/lock owner | `flow-deadlock`, SysRq-w, lockdep |
| Lock inversion | Earliest lockdep graph, held/acquired lock classes | lockdep, `flow-lockdown` |
| Data race | Two access sites, value transition, ordering primitive | KCSAN, targeted tracing |
| MCE/SError/APEI | Architecture syndrome plus hardware records | rasdaemon/EDAC/APEI/vendor tools |
| Regression | Good/bad kernel pair with same workload/config | upstream search, `git bisect` |

### 5.1 Exception and pointer faults

Use the exact faulting instruction, not merely the top C function:

```console
crash> bt -f
crash> bt -e
crash> dis -lr <function>
crash> struct <type> <address>
crash> kmem <address>
```

Map registers to the architecture ABI, calculate the effective address used by
the instruction, and verify the supposed object type with invariant fields and
allocator metadata or image-section bounds, as appropriate. Compiler
optimization and inlining can make a source-line-only explanation wrong.

When only an Oops is available, track what each saved register held at the
faulting instruction, including intermediate arithmetic and operand widths.
Do not assume argument registers still hold their entry values. Case 13 in
`case-studies.md` reconstructs a GRO offset from a preserved difference;
unobserved object fields must remain unknown.

#### 5.1.1 ARM64 single-bit pointer-corruption hypotheses

Use this path when a bad pointer appears one bit away from a plausible object.
Preserve the exception syndrome, fault address, PC, saved registers, `Code`
bytes, and this boot's `Kernel Offset` together. Analyze a candidate value
without modifying the dump or treating the candidate as an observed value.

1. **Close the fault-address calculation first.** Decode the exception class
   and read/write direction, then match the faulting instruction against the
   exact build. Calculate its effective address from the saved operands and
   compare it with the recorded fault address when valid for that syndrome.
   Trace the loads backwards to identify which object field supplied the bad
   pointer; obtain field offsets from matching-build types/disassembly.
2. **Quantify a justified candidate.** Explain why the expected field type,
   symbols, and address layout suggest that candidate. Compute
   `difference = observed XOR candidate`; exactly one differing bit requires
   `difference != 0` and `(difference & (difference - 1)) == 0`. Record the
   bit index. This proves a numerical relationship, not that the candidate was
   the original value or that a physical bit flip occurred.
3. **Validate the address and object semantics.** Use the same boot's KASLR
   offset and actual image/mapping bounds; a computed image base alone does
   not establish membership. Account for the pointer class, configured VA
   width, and applicable tagging/PAC rules; never blanket-mask high bits or
   apply userspace PAC masks to kernel pointers. VMCOREINFO can supply
   `KERNELOFFSET`, `KERNELPACMASK`, and `NUMBER(TCR_EL1_T1SZ)`.
   [ARM64 PAC](https://docs.kernel.org/arch/arm64/pointer-authentication.html),
   [VMCOREINFO](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html).
   A `sym` result can be a symbol plus an offset: validate the offset, object
   bounds/type, and expected member, not merely a recognizable symbol name.
   [crash sym help](https://crash-utility.github.io/help_pages/sym.html).
4. **Separate a table from its callback.** For a load through an operations
   table, distinguish the table-base pointer, the member-slot address, and the
   callback value stored there. A fault while reading the slot does not show
   that a callback value was loaded or that callback execution began. Keep an
   unread slot's contents unknown.
5. **Bound the conclusion.** Report a single-bit corruption hypothesis with
   separate confidence in the fault localization, reconstructed pointer, and
   physical cause. Keep software overwrite, UAF, DMA, and address-interpretation
   errors as competing explanations. Correlate saved RAS/ECC/controller records
   and object-lifetime evidence before attributing the failure to DDR hardware;
   unavailable or silent hardware records do not exclude a hardware fault.

See [Case 16](case-studies.md#case-16-arm64-single-bit-pointer-corruption-hypothesis)
for the published `generic_file_vm_ops` example. Agents use existing wrapper
disassembly and bounded reads on offline files. Unsupported `sym`/type/layout
queries require a precise handoff to an authorized human offline session;
vendor raw-dump loading is not permission to bypass the wrapper.

### 5.2 Hangs, lockups, and deadlocks

Soft lockup means kernel code failed to schedule for roughly
`2 * watchdog_thresh`; hard lockup means a CPU stopped servicing the watchdog
heartbeat. A hung task means a task remained blocked, usually in `D` state.
These are different failure modes and require different evidence.

Check collection overhead before adding more diagnostics. Slow serial output
and high-overhead tracing can themselves contribute to stalls, as documented
by the [RCU stall detector guide](https://docs.kernel.org/RCU/stallwarn.html).
Record console configuration, approximate output volume, affected CPUs, and
interrupt progress from existing evidence. Any live collection change still
requires exact-host/action authorization, bounded scope and duration, protected
output, and same-session cleanup or rollback. Do not suppress watchdogs merely
to hide their warnings.

A dependency cycle can involve page writeback or I/O completion, not just
mutexes. Recover the waited-on object and identify which operation must make
progress to release it; Case 15 in `case-studies.md` follows a page's mapping to
the inode whose writeback is blocked by reclaim.

Capture useful live state before forcing a dump when the machine still responds:

Writing `/proc/sysrq-trigger` changes a live host. Obtain explicit authorization
for the exact host and actions, confirm the output is being collected by an
access-controlled console/log path, and keep the sequence bounded. If that
authorization or capture path is unclear, provide these as operator steps only.

```bash
# all CPU backtraces, blocked tasks, held locks, memory state
echo l > /proc/sysrq-trigger
echo w > /proc/sysrq-trigger
echo d > /proc/sysrq-trigger
echo m > /proc/sysrq-trigger
```

The SysRq crash action deliberately panics the host. An agent must not execute
or automate it. Hand the final trigger to an authorized human using an approved
drill only after kdump, dump storage, out-of-band console access, workload
evacuation, and recovery procedures have all been verified.

#### 5.2.1 RCU Stalls: Compare the Same Grace Period

Use saved RCU splats before changing any detector. Group repeated warnings by
RCU flavor and **the same `g=` grace-period sequence**, then compare the named
CPU/task and its progress fields:

| Evidence | Working hypothesis and next check |
|---|---|
| `detected by N` | N reported the stall; analyze the listed blocking CPUs / `P<pid>` tasks first, not just N's detection stack. |
| `P<pid>` | A preemptible RCU reader task can block completion; check scheduling starvation and affinity as well as its read-side critical section. |
| `0 ticks this GP` | No scheduling-clock ticks were observed for this GP; investigate IRQ-disabled regions and timer/interrupt progress, not automatically hardware failure. |
| `softirq=a/b`, with b unchanged across same-GP reports | RCU softirq processing is not progressing; consider spinning/disabled IRQs and, on RT kernels, starvation of the softirq thread. |
| Repeated stacks share a stable upper section | Prioritize that stable code; distinguish it from varying interrupt/detector frames. |
| `All QSes seen` plus `kthread starved for` | Shift toward grace-period kthread starvation: the required quiescent states were already observed. |

The useful output is a differential: **GP → blocking CPU/PID → counter changes
→ stable stack → reader stall, IRQ/timer failure, or scheduler starvation**.
Use the target version's field definitions; do not hard-code `idle=` bit layouts
across kernels. No warning does not exclude a hang: this detector needs an
active grace period. Corroborate the selected hypothesis with existing IRQ,
scheduler, or task evidence; any new tracing follows the authorization and
overhead rules above. [RCU stall warning guide](https://docs.kernel.org/RCU/stallwarn.html).

### 5.3 Memory corruption and leaks

Choose instrumentation by environment and hypothesis:

- **Generic KASAN**: precise development-time OOB/UAF detection; high overhead.
- **SW_TAGS KASAN (ARM64)**: moderate-overhead testing on real workloads.
- **HW_TAGS KASAN (ARM64 MTE)**: low-overhead in-field detection or mitigation.
- **KFENCE**: sampled OOB/UAF/invalid-free detection with near-zero overhead;
  appropriate for long-running production fleets, but it may miss unsampled
  allocations.
- **Kmemleak**: finds possible orphan allocations; expect false positives and
  false negatives, and establish a clean baseline with `clear` then `scan`.
- **page_owner**: attributes page allocations and is especially useful when
  slab counters do not explain unreclaimable memory growth.

The tool that reports corruption found the detection point, which may not be
the instruction that first corrupted the object. Allocation and free stacks,
timestamps, and repeated reproductions are needed to close that gap.

For a failure during cleanup, inspect the earlier allocation error and every
release path, including callbacks. A poison pattern alone does not prove a
double free. Case 14 in `case-studies.md` combines the object's allocation/free
records with the error-path source to establish the sequence.

### 5.4 Races and locking

KCSAN samples instrumented memory accesses and can report both racing stacks
and observed value changes. Reports with an unknown origin may indicate
uninstrumented code or DMA, so treat them as evidence of a race candidate, not
automatic proof of a specific second writer.

Lockdep proves properties about lock classes and dependency chains it has
observed. Preserve the earliest lockdep splat: after lock debugging disables
itself, later state is less useful. Confirm that the implicated lock classes
represent the intended object instances and are not annotation mistakes.

### 5.5 OOM and memory pressure

Distinguish these before declaring a leak:

- growing process RSS;
- growing reclaimable or unreclaimable slab;
- page allocation fragmentation despite free memory;
- pinned pages or unreclaimable page-cache state;
- cgroup-local OOM versus system-wide OOM;
- deliberate `panic_on_oom` versus a secondary failure.

Correlate the OOM log with `kmem -i`, `kmem -z`, `kmem -s`, `ps -G`, cgroup
limits, and longitudinal metrics. A single end-state snapshot rarely proves a
leak.

## 6. Tool Escalation Matrix

| Tool | Best use | Important limitation |
|---|---|---|
| `crash` | Broad post-mortem inspection and familiar kernel commands | Manual repetition is hard to audit |
| `drgn` | Repeatable Python analyses over live kernels or vmcores | Requires trustworthy symbols/types and carefully bounded scripts |
| GDB kernel helpers | Source/assembly inspection, selected lists/tasks | Not a replacement for crash-wide subsystem views |
| pstore/ramoops | Survives reboot when kdump or storage path fails | Small circular storage; plan record sizes and retention |
| ftrace/kprobes | Temporal evidence for a reproducible issue | Can perturb timing and generate large traces |
| KASAN | Precise memory safety reports | Build/runtime overhead varies substantially by mode |
| KFENCE | Long-running sampled production detection | Sampling trades coverage for low overhead |
| KCSAN | Data-race detection | Sampling and missing instrumentation can hide or obscure races |
| lockdep | Lock ordering and context validation | Needs debug config and only reasons over observed chains/classes |

For uninitialized values, device-DMA corruption, allocation-error cleanup, or
rare pre-failure events, use the [targeted playbooks in the tools guide](debug-tools-guide.md#8-targeted-playbooks-close-a-specific-evidence-gap).
They specify the evidence each experiment adds and the limits of a silent run.

Use `drgn -c /path/to/vmcore` when the same structure traversal must be rerun
across many dumps. Keep the script, its version, and its output with the case so
the finding is reproducible.

## 7. Phase D — Hypotheses, Disproof, and Confidence

Maintain a small hypothesis ledger:

| Hypothesis | Supporting evidence | Disproof test | Result |
|---|---|---|---|
| Example: object freed before callback | poison pattern; callback stack | inspect alloc/free stacks under KASAN/KFENCE | pending |

Rules:

1. Keep at least one competing explanation until direct evidence excludes it.
2. Separate **fault site**, **corruption site**, and **root cause**.
3. Label missing or filtered memory as `unknown`, not `zero` or `not present`.
4. Give confidence as high/medium/low and state what evidence would change it.
5. Do not claim an upstream commit is the fix solely because its title matches;
   compare the affected code path and reproduce on both sides when possible.

## 8. Phase E — Known Fix and Regression Verification

Build a search signature from stable facts:

```text
panic class + first non-generic function + subsystem + kernel version
```

Search upstream documentation, lore.kernel.org, subsystem trees, stable release
notes, and distribution errata. Build the smallest useful query before using an
external service: remove customer names, hostnames, filesystem paths, addresses,
credentials, and proprietary module identifiers unless disclosure is explicitly
approved. Prefer public function names, the panic class, subsystem, and kernel
version. For a suspected regression:

1. Reproduce on the newest supported/mainline kernel when practical.
2. Reconfirm the last known-good build with the same config and workload.
3. Remove proprietary/out-of-tree modules when possible and record taint.
4. Bisect only after the good/bad endpoints are reliable.
5. Validate a candidate fix by reverting or applying that exact change, not by
   assuming correlation from a version upgrade.

The first bad commit can expose an older defect by changing object layout,
allocation reuse, or timing. Keep the **observed trigger**, **defect-introducing
change**, and **fix** separate in the report. The [kthread UAF investigation](https://gtucker.io/posts/2026-06-23-splitk-no1/)
illustrates this distinction: bisection implicated a pidfs layout change, while
the lifetime bug was in kthread exit handling. Test the proposed causal chain;
a successful revert alone does not prove where the defect originated.

Reproduction that could panic or reboot a host is an authorized human lab task.
Agents must not execute deliberate crash triggers; record human-supplied test
results and keep unperformed verification explicitly pending.

## 9. Root-Cause Report Template

```markdown
## Incident signature
- Kernel/build ID:
- Architecture/platform:
- Panic class and first fault:
- Taint/modules:

## Evidence quality
- vmcore completeness:
- symbol/module match:
- missing or filtered evidence:

## Timeline
1. Earliest anomaly
2. Trigger/workload
3. Primary failure
4. Secondary failures and dump transition

## Analysis
- Faulting instruction and effective address
- Relevant object/task/CPU state
- Competing hypotheses and disproof results

## Conclusion
- Root cause (or narrowest defensible cause):
- Confidence:
- Evidence that would change the conclusion:

## Remediation and verification
- Containment:
- Candidate fix/upstream status:
- Reproduction or regression test:
```

## Primary Sources

- [Linux kernel bug hunting](https://docs.kernel.org/admin-guide/bug-hunting.html)
- [Tainted kernels](https://docs.kernel.org/admin-guide/tainted-kernels.html)
- [Kdump](https://docs.kernel.org/admin-guide/kdump/kdump.html)
- [VMCOREINFO](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html)
- [Soft and hard lockup watchdogs](https://docs.kernel.org/admin-guide/lockup-watchdogs.html)
- [RCU stall warnings and diagnostic overhead](https://docs.kernel.org/RCU/stallwarn.html)
- [Magic SysRq](https://docs.kernel.org/admin-guide/sysrq.html)
- [Ramoops](https://docs.kernel.org/admin-guide/ramoops.html)
- [KASAN](https://docs.kernel.org/dev-tools/kasan.html)
- [KFENCE](https://docs.kernel.org/dev-tools/kfence.html)
- [KCSAN](https://docs.kernel.org/dev-tools/kcsan.html)
- [Kmemleak](https://docs.kernel.org/dev-tools/kmemleak.html)
- [Lockdep design](https://docs.kernel.org/locking/lockdep-design.html)
- [GDB kernel debugging helpers](https://docs.kernel.org/dev-tools/gdb-kernel-debugging.html)
- [Verifying bugs and bisecting regressions](https://docs.kernel.org/admin-guide/verify-bugs-and-bisect-regressions.html)
- [crash utility whitepaper](https://crash-utility.github.io/crash_whitepaper.html)
- [drgn user guide](https://drgn.readthedocs.io/en/latest/user_guide.html)
