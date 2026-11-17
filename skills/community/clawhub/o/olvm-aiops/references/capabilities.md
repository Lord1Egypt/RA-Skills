# olvm-aiops — Capabilities (18 MCP tools: 16 read, 2 undo)

Every diagnosis and listing is `[READ]`, `risk_level=low`; the harness's `undo_apply` is
`[WRITE]` (nothing records an undo in this release). All are wrapped by `@governed_tool`
(audited) and `@tool_errors` (failures come back as `{"error", "hint"}`), and each CLI command
calls the tool of the same name, so CLI calls are audited too. Engine: OLVM 4.5 / oVirt 4.5,
REST API `/ovirt-engine/api`, JSON with `Version: 4`.

Conventions in every payload:
- A field the engine did not report is `null` — never an invented `0`, `false` or `""`.
- Counts and sizes are real integers (the engine sends them as strings; they are converted).
- Times are ISO-8601 UTC (the engine sends epoch milliseconds).
- A listing with `limit` returns `returned`, `limit` and `truncated`; `truncated` is measured
  by asking the engine for one extra row.
- Findings carry `rank` (1 = worst), `severity`, `signal`, `cause`, `action`.
- A 2xx answer that is not JSON (a proxy error or SSO login page), or an empty body to a GET, is
  an error, never an empty collection.

## Diagnosis

| Tool | Reads | Findings |
|---|---|---|
| `engine_health_rca` | `/ovirt-engine/services/health` (no login), API root, `/datacenters`, warning+ events | high: health check not HTTP 200 with "DB Up"; medium: health check unreadable, engine clock more than 300 s from this machine's (`clockSkewSeconds`). Events naming no host, VM or storage domain: engine or CA certificate expiring = medium, alert = high, expired = critical; no full engine backup or backup too old = medium, backup failed = high; cluster failed HA reservation = medium; data-center status problems (979–993, 10811) medium/high while the data center is not up, superseded (`info`) once it is; a failed user login (114) = low with the repeat count in the signal and no invented count threshold, an account disabled or locked (160) = high; a manual `unlock_entity.sh` run (2024, written by the script at alert) = low with its own cause, never treated as resolving a later event; a storage-pool vdsm command failure (10803, no host in the template) keeps the event's severity, its cause names the command, and it is grouped per command so two different commands are two findings — wherever the row's refs send it; any other by severity. Also returns `engineVersion`, `healthServlet` and `summary` (hosts, storage domains, VMs: active / total). |
| `host_health_rca` | `/hosts`, `/events?search=severity>normal sortby time desc`, `/vms` (only when a guest-agent finding needs candidates) | high: `non_operational`, `non_responsive`, `install_failed`, `error`, `down`, `kdumping` (with `status_detail`); info: `installing`, `reboot`, `connecting`, `initializing`, `preparing_for_maintenance`, `maintenance` (the diagnosis cannot tell how long a host has been in one); medium: `reinstallation_required`; low: `update_available`; external status `error`/`failure` = high, `warning` = medium; events about a host alone from the last `events_window_hours` (default 24), one finding per host and code with the repeat count: host certificate expiring = medium, alert = high, expired = critical; time drift = medium; alert 9000 power management = low; any other = high (error/alert) or medium (warning), superseded (`info`) when the engine set the host to Up afterwards and it is up now. Certificate and time-drift alerts are never superseded. Event 10802 wraps any vdsm command, so it is grouped per condition (the command plus whether the message names the guest agent), not per code. One whose command name starts with `VmLogon` / `VmLogoff` **and** whose message names the guest agent is a guest problem, not a host fault: `low`, never superseded, and carrying `vmCandidates` (`{vms, returned, limit, truncated, total, scanTruncated, error}`) — the VMs the engine reports on that host, from one `/vms` read made only when such a finding exists. The event names no VM, so they are candidates, not the affected VM; `total: null` with `error` means the VM list could not be read, and `scanTruncated` means the VM scan was cut at 1000 so `total` is a lower bound (both are `null` when the read failed — there was no scan). `limit` is fixed; widen with `vm_list` `search="host=<name>"`. The same command failing for another reason (a vdsm transport timeout) stays a host finding at the event's own severity, but its cause names the failed command instead of calling the host the problem — the engine's template makes `${CommandName}` the subject and logs it against the host only because that is where the call ran. Every 10802 finding also carries `relatedVmEvents` (`{events, returned, limit, truncated, windowSeconds}`), the VM-naming problem events within `windowSeconds` (60) on the same host, each with a signed `secondsApart`: the engine records the operation's own failure against the VM (`vm_health_rca` reports that half) and nothing links the two, so they are paired on time and host — candidates, never a mapping. An event naming a different host is excluded, one naming no host is kept, and the list comes from the events already fetched (no extra read) and is returned even when empty. Both halves are read from the engine's English message; a translated engine falls back to a plain host finding. |
| `storage_capacity_rca` | storage domains + each data center's storage domains + warning+ events | critical: free space below `critical_space_action_blocker` GiB (engine refuses new disks and snapshots); medium: free % (the exact ratio, not the rounded `freePct`) below `warning_low_space_indicator`, external status warning; low: the engine has no crossable low-space threshold on the domain (it reports 0 for one that is not set, and 0 can never be crossed) — reported with the measured free space, separately for "no threshold at all" and "only the critical blocker, so no earlier signal", and never with a threshold this tool invented; committed > 100 % of capacity — low on its own (thin provisioning: a planning limit, and the signal carries actual use next to it), medium together with low space, when the promise cannot be kept; high: attached domain `inactive` / `unknown` / `mixed`, external status error; info: maintenance or transitions; medium: status unreadable (the action says retry when the data center view timed out). Events naming the domain and no VM: 970 deactivated by system = high, others by severity. Unattached domains are skipped. |
| `vm_health_rca` | `/vms`, warning+ events | high: `not_responding`, `unknown`, `paused` (storage first), HA VM `down`; medium: `image_locked`; info: transitions (`migrating`, `powering_up`, …); low: config change pending restart; VM events from the last `events_window_hours` (default 24), one finding per VM and code — superseded (`info`) when the VM started after the event (whatever its state now), or when the engine reported it back up (196 recovered from pause, 163 status restored) and it is up now |

Every warning-or-worse event inside the window lands in exactly one diagnosis: naming a VM →
`vm_health_rca`; a storage domain and no VM → `storage_capacity_rca`; only a host →
`host_health_rca`; none of those → `engine_health_rca`. A normal-severity event is never a
finding. `eventsTruncated` is true only when the event scan was cut while its oldest event was
still inside the window; `eventsOutsideWindow` counts the older ones that were read.

## Inventory

| Tool | Reads | Row highlights |
|---|---|---|
| `datacenter_list` | `/datacenters` | `status`, `compatibilityVersion`, `local`, `quotaMode` |
| `cluster_list` | `/clusters` | `compatibilityVersion`, `cpuType` (null until a host joins), `memoryOverCommitPct`, `ballooningEnabled`, `upgradeInProgress` |
| `host_list` / `host_get` | `/hosts` (`search` passed through) | `status`, `statusDetail`, `spmStatus`, `memoryBytes`, `maxSchedulingMemoryBytes`, `vmsActive`/`vmsTotal`, CPU topology, `osVersion`, `updateAvailable`, `reinstallationRequired` |
| `storage_domain_list` / `storage_domain_get` | `/storagedomains` + `/datacenters/{id}/storagedomains` | `status` + `statusSource` (`dataCenter` / `global` / null), `master`, `availableBytes`, `usedBytes`, `committedBytes`, `totalBytes`, `usedPct`, `freePct`, `committedPctOfTotal`, thresholds; `statusErrors` |
| `vm_list` / `vm_get` | `/vms` (`search` passed through) | `status`, `hostId`, `vcpus`, `memoryBytes`, `highAvailability`, `restartPendingForConfig`, `startTime`, `stopTime` |
| `vm_capacity_summary` | ordered `/vms` pages and `/hosts` | Compact VM/vCPU count, physical cores and assignment ratio; `complete=false` and null totals when required data are missing; never an atomic snapshot |
| `vm_stats` | `/vms/{id}/statistics` | `{name: {value, unit}}` — memory bytes, CPU %, network, `disks.usage`, `elapsed.time` |

Why storage status is joined: an attached domain has no `status` in `/storagedomains`
on a live engine; reading only that collection reports every attached domain as unknown.

## Activity

| Tool | Parameters | Notes |
|---|---|---|
| `event_list` | `limit`, `min_severity` (normal/warning/error/alert), `page`, `after_index`, `since_minutes` | Newest first (`order: newestFirst`). `page` N is read with the engine's page size (`max=limit`) and `truncated` by probing page N+1 — one extra row there shifts every page and hides a row at each boundary (seen live). `after_index` uses the engine's `from=` cursor and returns the events right after it **oldest first** (`order: oldestFirst`) — newest first would return the newest events above the cursor and skip the rest (seen live); it cannot be combined with `page`. `since_minutes` filters on each event's own time over a bounded scan; `scanTruncated` is true only when the scan was cut while its oldest event was still inside the window; the engine's `time` search is not used — on a live engine it returned all or nothing depending on date format. SSO session ids in login events are redacted. |
| `job_list` | `limit`, `status` (started/finished/failed/aborted/unknown) | The engine refuses `search` on `/jobs` (HTTP 400) and returns jobs oldest first; jobs are read in bulk, sorted newest first and filtered here (`scanTruncated`). |

## Governance

| Tool | Notes |
|---|---|
| `undo_list` / `undo_apply` | The harness undo log. This release has no writes, so nothing records an undo. |

## Not in this release

Writes of any kind. On a live engine, `POST /vms/{id}/start` answered HTTP 200 with
`status: complete` in 0.23 s while the VM reached `up` 72.7 s later, and a start issued right
after a disk add (201) was refused with 409 "disks are locked". A write tool must poll the
object (or correlate events through a `Correlation-Id` header, which the engine honours)
before reporting success.
