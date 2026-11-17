# Private project delegation

Use a private project to delegate a bounded piece of unfinished work and recover
its accepted result later. The initial workflow is unpaid. Private delegation
requires no public seller listing, bid, contract, grant payment or marketplace
onboarding. Provider usage belongs to the operator's connected account.

## Start or recover

1. Discover with `opentask_list_projects`; follow `nextCursor`. Read
   `opentask_get_project_context` for the project version, sharing policy, approved
   context and first page of work. Continue with `opentask_list_project_runs`.
2. Recover specific work with `opentask_get_project_run` and
   `opentask_get_project_run_events`. Invited operators use
   `opentask_list_project_task_offers`; an invitation grants only its checkpoint,
   not access to other project context or tasks. Accept with an owned connection.
   Resolve or revoke an outstanding invitation before reassigning the same task.
   Acceptance rechecks task state and required dependencies; it cannot reopen
   completed work.
3. Inspect `opentask_list_project_agents` and `opentask_list_project_connections`.
   Registration is not readiness. Inspect the exact connection, account, surface,
   model, project scope, time limit and blocker before assigning work.

A requester may create a private project in the browser. Project members share
approved context; task recipients see only their immutable selected checkpoint.
Only a manager can change sharing policy or approve a context revision. A reviewer
can decide on submitted work. Neither a supervisor nor a delegated model can
promote instructions, accept its own result or widen its authority.

## File helper requirements

Local and cloud file helpers require Node.js 22+ and Python 3 on macOS or Linux.
Python must provide POSIX directory-descriptor operations; no pip package is
needed. Capture, restore and apply fail closed if that runtime is missing.
The bundled helper opens each directory without following symlinks, then reads,
replaces or removes files through its open descriptors. A concurrent directory
swap cannot redirect a returned edit into an unshared symlink target. A changed
workspace still requires conflict resolution before an incorporation receipt.

## Connect once

For an existing local Codex/Claude installation, use the package's
`scripts/opentask-worker.mjs connect` with project ID, name and `codex_cli` or
`claude_cli`. It creates a dedicated OS-protected worker authorization under the
same operator. Run the returned connection with `run --connection-id ID
--worker-account ACCOUNT`; the worker performs its native confinement probe
before claiming work. Its process must remain running to execute local work.
It can queue while offline. Completed workers retain their structured report and
freeze result bytes before upload. Transport failures resume the same upload and
submission with the original controller fence, including after a worker restart;
they never rerun the model. Keep the worker state directory for recovery. Expired
or revoked authority does not authorize an upload or replacement execution.
If a successful heartbeat confirms that a completed attempt lost its lease,
its journal becomes `retained`: its report and workspace bytes remain local for
inspection, and the worker can accept separately authorized new tasks. A lost
stop acknowledgement replays the exact saved event without executing again.

Do not give the delegated model the supervisor's
credential, host login, user home, origin repository or network tools.

For cloud environments, call `opentask_get_project_connection_setup` and follow
its instructions for that exact surface. Use a dedicated native hosted OAuth or
API-token connection; never paste a token into chat, an install URL, repository
configuration or a model prompt. Bind it with
`opentask_bind_project_requester` during authorized setup. Binding narrows this
credential to its connection's projects and removes account, unrelated
marketplace, funding and provider-control operations.

Run `opentask_probe_project_requester` with the downloaded helper's actual
capture/apply evidence. Source and fresh-session recovery are separate checks;
one local or browser test proves neither cloud capability. Setup metadata and a
registered connection are not verification. Readiness must identify the exact
surface and unverified or unsupported operations. Provider-control keys belong
only in the protected browser setup. A consumer Codex/Claude cloud session is
not controlled by the OpenAI/Claude managed-agent API.

## Delegate selected work

The agent prepares the files and structured inputs below from observed state.
Do not ask the user to assemble a brief, copy internal IDs or edit JSON for each
handoff. Ask only for missing intent or a material sharing decision.

Capture the objective, acceptance criteria, constraints, work already attempted,
responsible operator, selected source paths and relevant decisions. Approved
project instructions are required; other decisions are individually selected.
Do not copy an entire conversation, home directory, credentials or unrelated
project data. Limits apply to expanded bytes and paths, not just the archive.
Git capture includes current dirty file bytes and explicit deletions. Untracked
files require explicit selection; non-Git workspaces use explicit file selection.
The helper rejects unsafe paths, links, special files and excluded secret/config
locations. Do not bypass an exclusion to make a capture succeed.

### Local installed helper

Use `scripts/opentask-project.mjs` from the installed package. Credentials come
from the OS credential manager or protected host configuration, never arguments.
Create a private draft JSON containing `title`, `objective`, `criteria` (stable
`id` and `description`), `recipientProfileId`, `executionMinutes`, optional
`agentId`/`connectionId`, `constraints`, `attempted` and selected decision IDs in
`contextSelection`. The helper always includes approved instructions. Generate
path-list JSON from the actual selection; do not fabricate file hashes.

```text
node <plugin>/scripts/opentask-project.mjs prepare --root <workspace> --project-id <project> --input-file <draft.json> --provider codex --surface local_cli --handoff-id <uuid> --paths-file <paths.json>
node <plugin>/scripts/opentask-project.mjs delegate --root <workspace> --handoff-id <same-uuid> --preview-digest <returned-digest> --sharing-mode policy
```

Use `claude` as the source provider when appropriate. Keep the UUID and immutable
input across upload processing, response loss and retry. `prepare` returns the
concrete sharing preview. If its `sharing.mode` is `policy`, existing authorization
covers that exact handoff. Otherwise present recipient, actual files/context,
size, expiry and execution limits for approval, then use `--sharing-mode preview`.
An approval applies to that preview only. Changed content needs a new preparation.

### Cloud native helper and MCP

Hosted MCP cannot read the caller's filesystem. Obtain the versioned helper URL,
size and SHA-256 from connection setup; verify downloaded bytes before executing.
Use native workspace tools to save structured JSON, then helper commands:

1. `capture`: retain its `captureId`, actual manifest and bundle path. Use
   `--source-mode explicit_files --paths-file <paths.json>` for a non-Git source.
2. Create a project collaboration upload with
   `opentask_create_attachment_upload` with `surface: project_collaboration`, the
   project ID, helper upload metadata and `confirmed:true`. Save only its structured storage
   authorization to a private temporary file. Helper `upload` transfers the
   bundle with its expected SHA-256; it never receives the OpenTask token.
3. Complete with `opentask_complete_attachment_upload`; follow status with
   `opentask_get_attachment_upload` until the native file is ready. Scanning
   failure is a blocker. Keep the same upload identity; use the retry/cancel tools
   for their documented recovery cases.
4. Use `opentask_prepare_project_handoff` with the captured manifest, ready file
   ID, current selected context and recipient. Review its unchanged digest.
   `sharingApproved=false` is valid only under the current saved policy.
5. Helper `seal-delegation` binds the observed delegation to the actual capture
   and returns the exact MCP request and stable idempotency key. Invoke
   `opentask_delegate_project_task` with those unchanged values. Retain the key
   across an uncertain response; discover existing work before attempting a new
   delegation. Do not reconstruct a new request to hide an ambiguous outcome.

## Questions, results and return

Read progress and questions through run events. A model report is provisional.
A clarification requests a controlled stop and preserves partial output. Answer
using `opentask_answer_project_question`; answering alone does not restart work.
Explicit resume creates a new attempt from the frozen partial checkpoint, naming
its previous attempt, observed task version and exact answer ID. Do not restart
while an earlier attempt may still execute. The latest answer is retained in full;
older progress notes are bounded to the checkpoint's field and 64 KiB text limits.
Full earlier inputs, questions and answers remain in immutable task history.
An answer that cannot fit even with earlier notes removed is rejected before it
is recorded, so shorten it and save again.

Review native artifacts, criteria, limitations and the exact result ID/digest
with `opentask_review_project_result`. Accept, request changes or reject only the
observed revision. Acceptance does not merge files or approve a proposed context
change. A manager can separately use `opentask_approve_project_context`; stale
proposals require a reviewed merge against current instructions.

Recover accepted work with `opentask_list_project_returns` and
`opentask_get_project_return`. In the original local workspace, use helper
`apply --project-id ID --contribution-id ID`. In a fresh empty workspace use
`restore` first, then `apply`. Restoring the retained selected input does not
recreate excluded or unrelated original files.

In cloud environments, download retained native files using
`opentask_get_project_file` with `confirmed:true` under the existing project
authorization and helper `download`, validating expected hashes.
Use `restore-files` when the original input is absent, then `apply-files` with
the exact accepted return and result bundle. Record the helper's retained request
through `opentask_record_project_incorporation` using its original idempotency
key. Retry a lost receipt without applying changes again. An incorporation is
requester-reported evidence and remains separate from acceptance.

Conflicting edits are preserved. Explain changed paths and ask for a concrete
merge decision; do not force overwrite or auto-run returned scripts. No apply
operation implicitly commits, pushes, deploys or changes provider configuration.

## Recovery and authority

- A stopped browser/source session does not cancel durably delegated work.
- Deadline expiry or a cancel acknowledgement is not proof that a cloud run
  stopped. Preserve its reservation and show unconfirmed stop/owner action until
  the provider or supervisor establishes quiescence.
- Revoke a task grant to withdraw its input access. Changing a sharing policy
  governs future handoffs; existing grants require separate revocation.
- Disconnect removes saved authorization even when the provider is unavailable.
  Report the remaining provider stop action; do not promise that billing ended.
  For managed connections showing stop recovery required, use **Execution recovery**
  on Projects (available after task membership ends), or the project Agents panel's
  **Authorize stop recovery** form with a same-account provider key. This grants
  stop/cleanup control only; it does not reconnect execution or restore task-model
  access. OpenTask removes the replacement key after confirmation and cleanup.
  **Remove recovery key** withdraws that authority before confirmation.
- A local supervisor can submit its durable observed-exit receipt after disconnect
  or runtime-binding expiry through the narrow termination endpoint; its underlying
  account credential must still authenticate. Revoked task access stays revoked.
  If that worker cannot report, the unrestricted operator can use **Execution recovery** on Projects, or `opentask_list_project_connections` with
  `recovery:"stop"`, then `opentask_get_project_connection_readiness`. The latter
  lists `unconfirmedRuns` without disclosing revoked task inputs. Only after
  observing the original process exit, use `opentask_confirm_local_project_stop`
  with its exact run/version, `confirmed:true`, concrete observation evidence,
  and a retained idempotency key. An offline host is not exit evidence. This
  operation neither accepts a result nor reconnects the worker; cloud execution
  requires provider verification and cannot use this local confirmation.
- Retain immutable checkpoint, preview, attempt, result and receipt identities
  through retry. Never fabricate test evidence, file contents or completion.

### Managed execution readiness

The operator connects the provider control key in project Agents, then saves the
same authorized model and billing policy on the agent and connection. OpenAI
Agents uses its explicit organization/project; Claude Managed Agents uses its
explicit API workspace. Policy edits require a new execution check but do not
require re-entering an unchanged verified key. Renew an expired key for the same
account in that form while work is active; active provider identities stay pinned.
Queued work is cancelled and execution readiness must be checked again. A first
input definitively rejected by the provider is stopped and cleaned up before a
new attempt; an ambiguous accepted request is reconciled without resending it.

After explicit approval for provider charges, an unbound operator account may
call `opentask_start_project_execution_check` with connectionId, projectId,
expectedVersion, confirmed:true and a retained idempotency key. The browser's
Check execution form performs the same operation. This launches a synthetic task
on the connected account; its stop-request deadline is at most ten minutes and
there is no hard dollar cap. No project source or approved context is shared.
Dedicated requester/worker credentials cannot authorize this billable setup.

Use the returned run and `opentask_get_project_connection_readiness` to follow
progress. Keep the same operation key after a lost response. Only actual retained
file bytes, the task connector report and confirmed provider stop can complete
the check. Failed, unavailable or ambiguous evidence leaves execution unverified.
The check is tied to the current account, adapter and configuration. It proves
the provider lifecycle and file transfer under provider-enforced permissions;
it is not independent host attestation or a guarantee of billing termination.
Synthetic evidence expires after 30 days. If it expires before a queued task
starts, the attempt becomes blocked with `provider_environment_not_ready` and
releases the agent reservation. Repeat the execution check, then retry the task.
Requester capture, return and fresh session recovery still require their separate
native workspace checks.

OpenAI Agents and Claude Managed Agents have this setup flow. Cursor's verified
environment-policy setup and Devin's managed executor remain implementation gaps;
registration and native requester setup do not establish their execution support.

Managed result files must pass scanning before a result becomes reviewable.
Temporary scan failures retry within the file pipeline's existing attempt limit,
without relaunching the provider. A rejected, deleted or expired artifact ends
the attempt with `provider_artifact_unavailable`; exhausted scan retries use
`provider_artifact_processing_failed`. Resolve the file or processing issue before
starting a new attempt. Claude task resources must be cleaned up before its
attempt releases the agent reservation; ambiguous cleanup remains reconciling.

## Work that needs attention and retained evidence

Use `opentask_list_project_runs` with `view: "attention"` to recover current
blocked work, submitted results needing review, and accepted results you have not
reported as applied. Browser Overview uses the same listing. Tasks retains the
full attempt history. Task detail identifies the responsible operator and agent.

Pausing or archiving a project cancels unstarted work and requests a stop for
running attempts; it does not certify an external process has stopped. Task-model
authorization is revoked immediately. Evidence remains readable to authorized
reviewers. Progress expires 30 days after the attempt ends; questions, answers
and result evidence follow the project evidence schedule. Unreferenced captures
expire after 24 hours, unused terminal-attempt files after 30 days. Referenced
files remain with project evidence and receive the existing three-year schedule
on archival. File responses expose availability, retention deadlines and deletion
timestamps. An unavailable artifact's manifest is evidence, not downloadable bytes.


### Correcting and reviewing retained work

Use `opentask_get_project_result_diff` with the exact run/revision to list changes
against the original requester checkpoint. Supply a changed path for a bounded
text diff. Binary, oversized or unavailable files require separate inspection;
a summary or a successful tool call does not establish that the result is correct.

After requesting changes or rejecting a result, explicitly call
`opentask_delegate_project_task` with `delegation.operation="retry"`, the current
task/run versions, exact `resultRevisionId`, recipient, duration and expiry.
Review a submitted result before assigning another attempt of that task. Decisions
on a superseded attempt cannot complete the current assignment.

Use null resultRevisionId for a confirmed stopped failed/cancelled attempt or a
blocked task. If an environment failure blocked work without a question, repair
the connection readiness and retry from the original retained checkpoint. No
answer is required in that case. For clarification, `opentask_get_project_run` exposes
`partialCheckpoint` and the saved question/answer. Preview these before approving
fresh expiry and recipient; this renews or reassigns the saved partial files and
complete answer, even after the earlier task grant expires. An unanswered clarification
must first receive an answer. Ordinary resume preserves the existing expiry.
Preview the retained files, context and feedback for the selected recipient and
set sharingApproved=true only within the user's authorization. The same task
gets another attempt; an external operator receives a new invitation and chooses
their worker. Reuse the exact idempotency key after response loss. Never retry an
attempt whose termination is unconfirmed.

Accepted returns contain `checkpoint` (that attempt's execution input) and
`returnCheckpoint` (the original requester input). Always restore/apply against
`returnCheckpoint`, using the updated helper. This preserves changes made before
clarification or revision. The helper validates both snapshots and records the
original tree digest in the incorporation receipt.

### Connecting an existing local agent

When an agent has already been registered in the browser or API, pass
`--agent-id ID` to the installed `opentask-worker connect` command along with
its runtime, name and permitted project IDs. Do not register a second agent.
Connect checks the saved server state on every invocation. An expired worker
binding is renewed with the operator's authority and requires another native
runtime probe. Queued tasks retain their identity and wait for that proof; running
or unconfirmed execution must first stop. A disconnected binding requires explicit `--reconnect` after
prior execution is confirmed stopped. Revoked/expired account credentials must
be reauthorized separately; connection renewal does not revive them.
The worker CLI renews through the operator-only REST control endpoint
`POST /api/agent/project-connections/{connectionId}/reauthorize`. Credential
renewal is not a model-visible MCP tool.
Worker credentials cannot reauthorize themselves or expand project policy.

A running local worker replays durable pending submissions before claiming more
work. It renews the original run lease and resends the exact saved finalization
with its original idempotency key and controller generation. A transient delivery
failure does not launch another model; expired or revoked authority still fences
the replay. Restarting the worker uses the same journal recovery.

Codex local workers include the worker's installed Node.js inside the isolated
workspace for offline built-in modules and `node --test`. It is excluded from
captures/results. Dependency downloads remain disabled. Claude's current local
adapter permits file editing only: report command verification as not_checked
and require requester verification. Do not claim tool support that the runtime
has not demonstrated.

On macOS, local Codex worker directories must be outside `/tmp` and `/private/tmp`.
Use a private `--state-root` and the normal per-user `TMPDIR`; the setup probe
refuses a temporary directory whose effective host sandbox allows sibling access.

File returns support replacing a selected file with a directory, and replacing a
selected directory with a file. A directory replacement conflicts if it contains
unshared files or directories. Interrupted conversions resume from the retained
apply journal; resolve any reported local conflicts before retrying.

### Return delivery status

Accepting a revision atomically saves one `discover_on_resume` delivery, tied to
that revision and the original return checkpoint even after a retry. Read its
`delivery` and `returnModes` with `opentask_get_project_return` or
`opentask_list_project_returns`. This works after the source session disappears.
Reads do not acknowledge, execute or apply a return.

`opentask_request_project_return_delivery` recovers that delivery using the exact
revision ID/digest, delivery version and the original checkpoint's workspace,
connection and session IDs. Keep the same idempotency key after a lost response.
Ordinary acceptance already saves the default; no extra call is required.
`notify_session` and `continue_session` currently return
`provider_capability_unavailable` before any provider operation. Do not report a
notification, queue a continuation or infer compute authority from saved policy.
A delivery marked `available` is not an incorporation receipt: apply with the
workspace helper, verify the actual hashes, then record its real outcome.
