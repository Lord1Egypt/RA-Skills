# Recover a JishuDB MCP connection

Use this workflow when JishuDB tools are absent, client configuration is empty,
or setup or a task encounters an unavailable connection.
Keep the user's intended machine and knowledge base explicit. A connection
repair is complete only when the actual host client can use that service.

## Establish the target before changing it

Inspect the active client entry and its actual source (user, workspace, managed
settings, or process override), with secrets redacted. Distinguish the machine
running the MCP client from the machine running this diagnostic agent: loopback
belongs to the client, not necessarily the agent's shell. Run local probes on
the intended service machine through an already authorized remote connection
when appropriate. Never substitute the diagnostic agent's own localhost.

Reuse a target already chosen by the user. If no target was selected and no
client entry or Desktop installation exists on a supported local machine,
continue to the local Desktop read-only installation plan in [setup guide](../setup.md).
Present the concrete plan for any missing installation approval; do not ask a
separate target-selection question merely because this is a first install.

If a configured target fails or conflicts with the request, explain that target
and observed failure, then offer only relevant recovery choices: repair the
existing local Desktop, repair the selected remote service, use a user-supplied
remote URL, or plan a local Desktop installation. Ask only when these represent
a genuinely unresolved choice. Never replace an explicitly selected service.

A remote URL in old configuration or memory is neither a new user instruction
nor proof of the wrong target. Do not probe remembered ports, copy old
credentials, silently switch databases, or claim readiness before host calls.
No answer to a required choice or approval means it remains unresolved;
elapsed time is not consent. Missing tools do not authorize local-only output.

## Diagnose the failing layer

Use the endpoint-resolution and health-identity rules in [setup guide](../setup.md). Report the
observed error and next action; keep hypotheses separate from verified causes.
Retain sanitized exit codes, signals, elapsed times, and error causes where
available, never authentication headers or full environment dumps.

| Observation | Check and recovery |
| --- | --- |
| No host entry or wrong effective entry | Locate the configuration actually loaded by the client. Resolve overlapping scopes or overrides before editing. Offer a target choice if unresolved. |
| File contains JishuDB but the host's MCP list does not | This is an unloaded configuration, not yet an OAuth failure. Use the host's supported reload/refresh or configuration-save action and read its list back. If no such action is exposed, return `USER_ACTION_REQUIRED` for a safe user-operated reload/import or restart. Do not ask the user to trust an entry that has not appeared. |
| DNS failure, no route, or connection timeout | Verify the selected host and service reachability from the client. Ask for an updated address or restoration of the required network only when needed. A private IP or timeout does not prove a VPN or subnet cause. |
| Local connection refused | Resolve `desktop-endpoint.json`; check the installed app and listener. Start the existing app within the authorized scope and current user's desktop session. An SSH service-session process is not proof of a working desktop launch. |
| App uninstalled; endpoint or data-location JSON remains | Preserve the files. The endpoint is a port preference; the data bootstrap locates retained data. Use the installation helper's reviewed plan: valid retained data selects an interactive data-preserving reinstall, while an endpoint alone can be reused by a fresh install. Do not delete data or configuration to satisfy fresh-install checks. |
| Installer succeeded; helper failed before Desktop launch | Verify the installed version/revision, bootstrap and endpoint, then continue the authorized launch. Do not rerun fresh installation over the newly created application/data directories. |
| Service was healthy inside a launch command but is gone in the next call | Inspect process lifetime and startup logs; host child-process cleanup is a hypothesis until verified. Do not diagnose this as missing OAuth, repeatedly reinstall, or ask the user to edit MCP JSON. Verify a supported launch survives the original tool call before continuing. |
| `desktop_launch_failed` after installation | The Windows helper delegates a private shortcut to Explorer and preserves the approved presentation mode. Inspect the original shortcut/COM/shell diagnostic and installed-state receipt. Do not fall back to a detached child, disable host sandboxing, create a scheduled task, or run the installer again. If shell delegation is unavailable, ask the user to launch the installed app from its normal shortcut and verify health in a separate call. |
| App executable is absent but its directory contains Python bytecode caches | Use the reviewed retained-data reinstall plan. The helper admits bounded recognized uninstall caches without deleting them; a directory alone is not a working installation. Unknown files or application binaries require review. |
| Native identity/ACL helper fails | Preserve its error category, operation and underlying OS code. Use the packaged asynchronous system-tool implementation; do not infer a missing runtime or OS-policy denial from `EBUSY`, replace Node, or bypass SID/ACL checks. |
| ACL hardening fails and a later plan reports `download_locked` | Inspect creation time, owner, permissions and live holders before calling a lock stale. Current helpers clean up only their own failed new files. If `cleanup.status` is `manual_recovery_required`, stop for authorized recovery of that exact file; preserve `release-floor.json` and all user data. A passing isolated probe does not establish the cause of the original denial. |
| Desktop startup dialog or executable check failure | Inspect the exact bundled executable, manifest, launch context, and sanitized startup diagnostics. Distinguish missing files, identity mismatch, access denial, nonzero exit, signal, and timeout. A process or successful standalone version check does not prove Desktop started. |
| Health response is not JishuDB, redirects, or a protocol response is invalid | Stop credentials and writes to this target; resolve the intended service/path. Do not bypass identity checks or TLS verification. |
| `401` | Separate missing authentication from rejected credentials; do not guess expiry or revocation. Follow the advertised authorization flow for this exact target. |
| `403` or missing write tools | Distinguish origin/policy rejection from proven scope or KB-access insufficiency. Request the necessary scoped authorization; do not reinstall or infer privilege from a profile label. |
| Browser consent succeeded; client still says Authorizing | Check whether the original callback arrived and automatic return is still pending. Do not start Connect again merely to dismiss the spinner. If the authorization page reports a return failure, use its existing return link once; distinguish missing callback, token-exchange error, and tool-discovery failure. |
| Health and direct MCP probes work but host tools are unavailable | Check host-loaded URL, authorization, trust, transport, and cached discovery. Reconnect through the host; do not report curl-only success. |
| `429` or temporary upstream failure | Respect `Retry-After` and retry only the affected read-only probe within the bound below. |

Do not repair startup by opening Desktop SQLite in another service, replacing
bundled executables with system binaries, turning off security checks, or
raising timeouts without evidence. If a later launch succeeds but the earlier
cause is unknown, report recovery and that uncertainty separately.

## Apply the smallest authorized repair

Read-only diagnosis needs no repeated confirmation. Use existing authorization
for the selected target and repair. If a decision is missing, present the
concrete proposed change and its effect on which knowledge base is used before
requesting that choice. Installation, upgrades, data changes, and additional
privileges retain their own scope and presence gates from [setup guide](../setup.md).

Prefer the host's supported configuration UI or command. For an authorized file
edit, back up privately, preserve unrelated entries and permissions, detect
concurrent changes, and atomically replace only the selected entry. Re-read the
effective configuration; changing an unused file is not a repair.

### Load WorkBuddy configuration

Do the configuration and loading work yourself when supported controls are
available under existing authorization. Inspect exposed host-management tools
and, when available, the current native UI. Do not infer that the user must
edit JSON from a missing JishuDB tool search result. If the file is correct,
preserve it and locate the loading action instead of rewriting it.

After the write, verify the host's in-memory registration separately. WorkBuddy
5.7.7 was observed to cache user MCP entries: its `mcp:list` operation does not
reread `mcp.json`, while `mcp:refresh` does. These are implementation identifiers,
not an instruction to invent a CLI command or call an undocumented private
transport. Prefer an exposed native refresh/configuration UI; if unavailable,
provide the exact user action needed. Reopening the list or creating a new chat
alone does not establish reload. For other clients, verify their own behavior.
Record the selected entry's actual name, URL and transport before continuing to
trust or OAuth; never equate an existing JSON key with an entry in the UI.

Historical native path verified in WorkBuddy 5.7.7; use only if the installed
version exposes these controls and the entry is actually unloaded:

1. Open **Connectors > Custom connectors > Add MCP**. Despite the button name,
   this opens the full configuration editor, not a request for a duplicate entry.
2. Confirm the editor's displayed configuration path and preserve all entries.
   If it already contains the correct externally written JSON but **Save** is
   disabled, make a whitespace-only edit outside JSON strings, then **Save**.
3. Select **Back to MCP List** and confirm the named JishuDB entry. A first-time
   entry may now display **Trust**; that is the user's separate trust checkpoint.
   It does not establish server health, OAuth completion, or tool availability.

Use this UI yourself when available under the user's existing configuration
authority; leave the separate Trust and OAuth prompts to the user. If no
supported control is accessible, state the missing capability and ask for only
the next verified loading action. Say "configuration saved; client entry not
yet loaded" rather than asking the user to recreate JSON. Do not send the full
historical tutorial by default or promise that a reload fixes an offline DB.
Do not use private IPC,
auto-trusting import calls, or a forced application kill to imitate this action.

### Reauthorize and verify

When changing service identity, do not carry the previous target's manual Token
or OAuth grant to the new service. Remove a stale static Authorization header
from the selected entry with a protected backup; use the client's native
reauthorization for the selected endpoint. Do not read/copy OAuth tokens or
other clients' secrets. Validate metadata without credentials or redirects,
then offer browser OAuth when supported, with protected manual Token entry as
the explicit alternative under the existing authorization rules. Never click
agreement, OAuth consent, or device-owner prompts on the user's behalf.

Reconnect through the host's supported action and refresh its tool catalog.
If a restart would interrupt active work, explain the need and let the user
restart at a safe point. Do not terminate the host or edit conversation history
to force a reload. A required host action is `USER_ACTION_REQUIRED`.

After an observed recovery condition changes, retry the affected read-only
probe with a finite timeout, at most twice per unchanged failure in this task.
Do not repeatedly restart applications, reinstall, or reconnect with the same
failure. If a diagnostic connection drops, stop remote mutations and recheck
identity after recovery. Resume after a new user action or new evidence.

## Verify and resume the original task

Verify the loaded host entry, authenticated initialize, `tools/list`, and
`kb_get_capabilities`. For a write task verify write tools and access, then call
`kb_list` to resolve the intended KB on this service. KB IDs and permissions
from the previous service are not portable. Follow runtime-readiness checks
before importing; do not use synthetic writes to prove connectivity.

Keep four results separate: configuration saved, client entry loaded, user
authorization completed, and required host tools callable. Stop at the first
unverified result with its specific next action. Only the final result plus
required task readiness can be reported as `READY`.

Resume the existing task with its original output directory and stable source
identities. Reconcile ambiguous prior writes through the original service
before retrying; do not replay writes blindly against a different database.
Existing local artifacts remain pending archival until the intended write and
readback succeed. If connection setup failed before generation, pause that
workflow rather than silently producing a local-only deliverable.

Report the verified endpoint and last successful layer. Use `READY` only after
actual host calls and required readiness pass; otherwise give
`USER_ACTION_REQUIRED`, `BLOCKED`, or `FAILED` with the exact outstanding action.
A valid saved URL, running process, healthy endpoint, and completed import are
separate observations.
