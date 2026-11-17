# Agent guardrails — running olvm-aiops with a smaller / local model

Guardrails written into a prompt are requests; guardrails in the tool are guarantees. This page
separates the two so a prompt only spends tokens on what the tool cannot enforce.

## Authorization is not this tool's job — decide it where it belongs

olvm-aiops does not decide what an agent may change. This release has no write tools at all,
and when writes arrive the boundary will still be the engine account: connect a user with a
read-only role (for example `ReadOnlyAdmin`) and the engine refuses every change regardless of
what any model decides. Do not rely on prompt wording for this.

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A value the engine did not report comes back as `null`, never as `0`, `false` or `""`. |
| "Numbers from the API are strings, convert them" | Counts, sizes and flags are converted to real integers and booleans; times to ISO-8601 UTC. |
| "Tell me if the output was cut off" | Every limited listing returns `returned`, `limit` and a measured `truncated`; scans report `scanTruncated` / `hostsTruncated` / `vmsTruncated` / `domainsTruncated` / `eventsTruncated` (the event flag means the window itself was cut). |
| "Start with the worst problem" | Diagnoses return findings with an explicit `rank` (1 = worst). |
| "Explain why something was flagged" | Every finding carries the measured `signal`, a `cause` and an `action`. |
| "Don't treat a host being installed/rebooted as broken" | In-progress host states are `info` findings; alert 9000 (no fencing hardware) is `low`. |
| "An old failed start doesn't mean the VM is broken now" | A VM event is superseded (`info`) when the VM started after it or the engine reported it back up; a host event when the engine set the host to Up afterwards; a data-center status event once the data center is up. Events older than `events_window_hours` (default 24) are not findings. |
| "Don't blame the host for a storage or VM problem" | An event that names a VM or storage domain is not attributed to the host that ran it; repeats of one code on one host are one finding with a count. Event 10802 names no VM but reports one vdsm command, and its storage-pool sibling 10803 names no host at all: their `cause` names that command rather than calling the host the problem (read from the engine's English message — a translated engine falls back to the plain host wording), and `relatedVmEvents` offers the VM-level failures the engine logged beside it. **It is not downgraded** — only the guest-agent condition is, because only its message names the subject; for every other command the event's severity is kept, so you still have to read which of the two it is. |
| "A login page is not an empty inventory" | A non-JSON success response is an error, never an empty list. |
| "Check the engine itself — certificates, backups" | `engine_health_rca` reads the health check and the clock, and reports the engine-wide alerts no other diagnosis sees. |
| "Storage status: check the data center, not the global list" | Storage status is joined from each data center; `statusSource` says where it came from. |
| "A manual repair isn't an engine fault" | Event 2024 (`unlock_entity.sh` run by hand) is written by the script at `alert` but reported `low` with its own cause: it records a lock cleared in the database. It is **not** treated as resolving anything — the entity is named only in its text, so a later failure on the same id (such as 10803 "Image does not exist") is still reported at its own severity. |
| "A failed login isn't an engine outage" | A user failing to log in (event 114) is `low` with the repeat count in the signal, so one mistyped password does not make `engine_health_rca` report the engine unhealthy; an account that is disabled or locked (160) is `high`. No count threshold is applied — how many failures matter is your judgement, and the engine records no threshold either. |
| "Don't leak credentials" | Passwords are encrypted at rest, tokens stay in memory, SSO session ids in events are redacted. |
| "Log what you did" | Every call — MCP and CLI — writes an audit row to `~/.olvm-aiops/audit.db`. |
| "Don't loop on the same call" | The runaway guard trips a circuit breaker on tight repetition. |

## What still needs a prompt

1. **Call the diagnoses first.** For "what is wrong", call `engine_health_rca`,
   `host_health_rca`, `storage_capacity_rca` and `vm_health_rca` before reading raw lists.
2. **Report in rank order and quote the signal.** Do not paraphrase numbers.
3. **Severity words mean what they say.** `info` means in progress or superseded. `low` means the object the finding is on is not at fault — it is not an incident for that host or domain, but its `action` can still be work (a guest-agent finding is `low` and asks you to check the guest).
4. **A `null` is unknown.** Say "not reported", never "zero" or "none".
5. **Do not claim completeness when a scan was cut.** If any `*Truncated` is true, say the answer
   is partial and how to widen it (`limit`, `events_limit`, `events_window_hours`, `page`).
6. **Follow events with the cursor.** Pass the highest `index` returned as `after_index`; the
   events after it come back oldest first — repeat while `truncated` is true.
7. **`vmCandidates` is a candidate list, not an answer.** A guest-agent event names no VM;
   say "one of these VMs", never "the affected VM is X" — even when only one is listed. It has
   no `limit` knob: for the whole list on a busy host read `vm_list` with `search="host=<name>"`,
   and if its `error` is set or `scanTruncated` is true, say the candidate list is incomplete.
8. **`relatedVmEvents` is the other candidate list.** Event 10802 reports one vdsm command,
   and the engine logs the operation's own failure against the VM as a separate event — so
   `host_health_rca` and `vm_health_rca` each hold one half of the same incident. The field
   pairs them on time and host only: say "possibly the same operation as", never "this host
   finding is about VM X". An empty list means the engine logged no VM failure within
   `windowSeconds`, not that none was looked for.
9. **A 10802 finding is about the command, not the host.** Its `cause` names the command.
   Do not report it as "this host is failing" unless the host's own status, external status
   or flags say so — and do not report it as harmless either: only the guest-agent condition
   is downgraded, because only its message names the subject.
10. **Over-commit is not the same as low space.** An over-committed domain with free space left
   is a planning limit; only a low-space or critical-blocker finding means it is running out.
11. **Do not fabricate write operations.** This release cannot start, stop, migrate or snapshot;
   say so instead of describing a result.
12. **Keep VM pages small for agents.** Use `vm_list(limit=20)` and follow `nextPage`.
    If a page or continuation metadata is clipped, do not compute totals or rankings from
    the visible subset. For VM count, configured vCPUs and host-core assignment, use
    `vm_capacity_summary`; quote totals only when `complete` is true, and state that
    `snapshotConsistent` is false even for a completed scan.

## Recommended setup for a local model

```text
You operate an Oracle Linux Virtualization Manager engine through olvm-aiops tools.
For "what is wrong" questions, call engine_health_rca, host_health_rca, storage_capacity_rca
and vm_health_rca first. Report findings in rank order; quote each finding's signal exactly. info and low are
not incidents for the object they are on, but a low finding's action can still be work. A null value means the engine did not report it — say "not reported".
If any truncated/scanTruncated/hostsTruncated/vmsTruncated/domainsTruncated/eventsTruncated
field is true, say the answer is partial. To follow new events, pass the highest index returned
as after_index and repeat while truncated is true. vmCandidates lists VMs the event could be about: say "one of these", never "the affected VM".
A 10802 finding is about the vdsm command its cause names, not about the host; relatedVmEvents pairs it with VM-level
failures the engine logged beside it on time alone: say "possibly the same operation", never "this host finding is about VM X".
An over-committed storage domain with free space left is a planning limit, not a shortage.
You cannot change anything in this release; never describe a change as done.
```

Connect the tool with a read-only engine account as well — the prompt is not the boundary.

## If your model still struggles

- Prefer the CLI (`olvm-aiops engine health`, `host health`, `storage capacity`, `vm health`): shorter output
  than MCP JSON.
- Lower `limit` / `events_limit` so each result fits the context window; the truncation fields
  still say when more exists.
- Ask one question per turn; each diagnosis already combines the reads it needs.
