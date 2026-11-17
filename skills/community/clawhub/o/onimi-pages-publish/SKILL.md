---
name: onimi-pages-publish
description: Save, check, and publish Onimi Pages or Onimi Slides through browser-authorized Remote MCP / 通过浏览器授权的远程 MCP 保存、检查并发布 Onimi 网页或 Onimi Slides 演示文稿。
metadata:
  version: "0.3.1"
---

# Onimi Publish · Pages and Slides

Use the Onimi Pages Remote MCP tools at `https://onimi.ai/mcp`. Never ask for an API key, bearer token,
authorization code, refresh token or session cookie in chat, and do not turn the HTTP routes into raw
`curl` instructions. The MCP client owns OAuth discovery, PKCE, browser consent, refresh and credential
storage.

Use the conversation language for progress and results. Keep tool names, IDs, hashes, status values and
visibility values exact. Artifact language is a separate user choice.

## Optional Agent stage reporting

If the Agent host can observe these stages, use the optional in-memory helper described in
[stage-observer.md](references/stage-observer.md). The helper does not collect events by itself or
replace a real WorkBuddy report receipt.

When the connected service exposes `onimi_report_agent_event`, report each eligible stage that this
Agent directly observes once, as soon as its stated trigger has occurred. This is optional product
analytics, separate from OAuth permission. The server checks
the current per-Agent analytics choice and privacy signals on every report; a missing tool, suppressed
receipt, timeout or error never blocks installation, creation, connection or publishing. Do not prompt
for analytics consent as a prerequisite or retry a failed report to make the task appear successful.

Use fresh random UUIDv4 values for the short-lived analytics `taskId`, `operationId` and each `reportId`.
They are not the project ID, journal task ID, client/account ID or a hash of user content. Keep a stable
`taskId` only for one observed task; use a stable `operationId` for one observed operation and keep its
`reportId` unchanged if a delivery retry is necessary. Discard these analytics IDs after the task.
Submit `locale`, those three IDs, the exact event name and only its fixed fields to the report tool.
Do not synthesize an event from an MCP request or a journal entry: first verify the client-side fact
described below. If the tool is unavailable at that moment, or a required fact or clock is unknown,
omit that stage; do not backfill it from a later server response.
Send only the event's fixed enum fields. Never send prompts, source, body, URLs, notes, names, tokens,
error text or user identifiers. If the host indicates DNT or GPC, preserve those request signals;
do not bypass a host privacy setting through another connection.

- `onimi.task.started`: only after the user actually confirms an install, Page, Slides or update task.
  `task_kind` is `install|page|slides|update`. A generic greeting or an unconfirmed new project is not
  a start.
- `onimi.capability.ready`: only after checking the actual local Creator/Publish module and its usable
  entrypoint. Set `module` to `creator|publish|suite` and `reused` according to that check. An MCP
  connection or advertised Skill name does not prove local readiness.
- `onimi.authorization.waiting`: only when this client actually opens the browser authorization and is
  waiting, with observed `reason` `first|expired|revoked|account_changed|scope_changed`. With no valid
  bearer yet, this tool is unavailable; omit the event rather than claiming it retrospectively.
- `onimi.connection.result`: report `ready` only after this client checks `onimi_get_connection` and
  confirms the current account and needed scopes; set `reused` from the observed client connection.
  Report another allowed result only when directly observed and the report tool remains authenticated.
- `onimi.preview.first`: only after the first actual Page or Slides preview is visible to the user.
  Set `artifact_kind` and measure `agent_ms` and `user_wait_ms` separately with a monotonic clock;
  exclude browser authorization and other user waiting from Agent time. If visibility or either clock
  is unknown, omit it.
- `onimi.publication.result`: only from a definite response for the exact prepare or activation
  operation. Use `result` `pending|active|rejected|conflict|failed`, actual `retry` state, and measured
  Agent milliseconds excluding user wait. A timeout or unknown result is not `failed` or `active`.
  Keep one definite result per operation; prepare and activate are distinct operations.

Do not report `onimi.publication.confirmed` from an Agent tool call. The browser confirmation event has
its own fixed revision and access-summary check. A report receipt says only whether optional telemetry
was accepted, duplicated, suppressed or uncertain; it is never proof of business success. If the tool
is absent on an older connection, continue the task normally.

## Connect and select the target

Read [installation.md](references/installation.md) for English connection help or
[installation.zh-CN.md](references/installation.zh-CN.md) in a Chinese conversation. On first use, let
the host open the authorization page; the user approves scopes in the browser. First inspect the host's
real connection state and reuse a valid connection only when it belongs to the same client/account and
covers every scope required by the current task. Do not authorize Creator and Publish separately for
the same scope set. An expired or revoked connection, a different client/account, or a newly required
scope needs consent again. Existing old publish consent does not imply `draft:read`, `draft:write`,
`template:read`, `release:read`, or `collaboration:manage`.

Before opening consent, state the current assistant/client, the Onimi account when known, the requested
scopes, what they permit and where the user can disconnect. `draft:read` can return private author
source including speaker notes, hidden slides or hidden content; `draft:write` can save a new private
revision; `template:read` can acquire an entitled governed template; `release:publish` can submit and
activate releases; `collaboration:manage` can change participant links, invitations and access policy.
Never describe that combined scope set as only “permission to publish.” Request the smallest set needed
for the task and let the browser consent page remain the authority.

Treat suite preparation, connection and task continuation as separate recoverable stages: preparing
Creator/Publish, waiting for the user in the browser, verifying the connection, then continuing the
original task. Report only observed stages, never a percentage. Verify with the least sensitive safe
read: call `onimi_get_connection` and compare its account and effective scopes. If an older deployed
service does not expose it, `onimi_list_projects` is a compatibility fallback and an empty list is
success. Do not read a private draft or create a project as a connection test. The connection tool's
`installedModules: "client-local-check-required"` means inspect the actual local Skill directory; never
infer installation from the server. If the user cancels, preserve the local artifact and these exact
continuation identifiers when present: `resourceType`, `resourceKey`, `resourceVersion`, `locale`, and
optional paired `themeKey` / `themeVersion`. Never put prompts, private material or credentials in the
continuation URL. Retry only the failed stage and do not repeat installation or consent already shown to
be complete. Revoking the connection stops later cloud operations; it does not delete or unpublish
existing work.

If browser consent is canceled, expires, or cannot complete because the network is offline or times
out, stop cloud operations and say which stage failed and who can retry it. Keep the original task and
local draft. If a task journal already exists, run `task-state.mjs pause` rather than `cancel`; `cancel`
is only for abandoning the publication/update intent. On retry, inspect the current client's real
connection, obtain fresh consent only if the account or scopes still require it, and verify with
`onimi_get_connection` before running `task-state.mjs resume`. For an uncertain earlier cloud write,
read the server state first and retry only its original request and mutation ID after resuming. Do not
turn a connection failure into permission to continue or into a publication success claim.

If the Agent host or user cancels an in-flight MCP request, a missing response does not prove that the
server canceled the write. Treat the result as uncertain: retain the same task journal, exact request
and mutation ID, mark the operation `uncertain` when possible, and `pause` the task. A later request to
continue must inspect that journal and reconcile the server result before retrying the same mutation.
Do not initialize a new task or generate a new mutation ID for the same publication intent because the
client-side call was canceled. A user who explicitly abandons the intent may stop here; do not make
another cloud write on their behalf.

Before any project or release write, establish the target intent from the whole conversation: update
one existing project, or create one new project. A generic request to publish does not mean create a
new project. Reuse an explicit earlier choice of target, project name or access; do not ask the user to
confirm the same choice again.

Call `onimi_list_projects` first. Resolve an explicit project UUID exactly; resolve a dashboard/editor
URL by its embedded UUID; resolve an audience URL by its exact project slug; or resolve an explicit
project name only when exactly one returned project has that name. Never use a partial/fuzzy name match
for a write. If the reference has no match or multiple name matches, show the short candidates and ask
which one. If the user has not chosen update versus create, ask once, combining only the missing facts:
for an update, the existing project name/ID/URL; for a new project, its name and intended access
(`public` means listed in Explore and open to anyone, `unlisted` means open to anyone with the link, or
`private` means owner/grant access). Do not ask for new-project name or visibility on an update. An
explicit controlled-sharing choice establishes `private`; explain that consequence without asking a
redundant visibility question.

Call `onimi_create_project` only after the user explicitly chooses a new project and its name and access
are known. A title, filename or page heading is not a confirmed project name unless the user made it the
project name. Derive a valid unused slug from the confirmed name and state it if it was inferred. Plan
`createProject` in the task journal and pass its UUID as the required `idempotencyKey`; an uncertain
retry uses the same UUID and exact request, so it resolves to the original project. The tool creates the
project as `private`; keep it private through draft/publication preparation, then use
`onimi_set_visibility` to apply an explicitly chosen `public` or `unlisted` access. If that tool is not
available, do not create a project whose requested access cannot be completed solely to make progress;
offer the dashboard fallback. A confirmed `private` project needs no visibility mutation.

For an update, keep the same project ID, draft and release history, visibility, grants, and controlled
data policy unless the user explicitly requests one of those settings to change. Saving or publishing
new bytes creates a revision/release in that project; it is not permission to create a replacement
project. State the resolved artifact, project and actual access before the first external write when any
part was inferred.
Set the supported `artifactKind` field to `page` or `slides`; older callers default to Pages.
Keep artifact kind separate from content tags. Add concise user-relevant tags (such as `work-report` or
`lesson`) on project creation. Dashboard supports type and tag filters. After a successful draft save or
publication, return the service-provided `editorUrl` so the owner can continue editing. It requires
owner login and is not the audience sharing URL. Current Slides editing is owner-only, without invited
editors or real-time coediting; audience links never grant draft access.

Check the tools actually discovered from the connected service before choosing either workflow.

## Persist and resume a multi-step task

Do not rely on conversation memory for a cloud write that spans tool calls, publication preparation or another
session. Before the first write, initialize `scripts/task-state.mjs` with the artifact kind, exact
update `projectId` or confirmed create intent, and the six public resource-selection identifiers when
present. The script stores state under `$XDG_STATE_HOME/onimi-pages/tasks` or
`~/.local/state/onimi-pages/tasks`, makes the directory `0700`, writes the task file atomically as
`0600`, and returns its `taskId` and path. Keep that task ID in the user-visible handoff.

Pass command input through an absolute JSON file outside the project checkout and remove that command
file after use. The durable task file stores only a short task summary, exact IDs/versions/hashes,
mutation UUIDs, status and a step-specific safe receipt. It rejects arbitrary receipt fields. It never
stores source, HTML, manifests, prompts, notes, email addresses, OAuth material, invitation codes or
grant redemption paths. Use `digest --file <absolute-path>` to hash a request payload without copying
it into the task state.

For `createGrant`, finish with the actual non-secret `projectId`, `grantId`, `grantVersion`
and returned `expiresAt` when present. The grant tool does not return a publication-style
`status`; omit it rather than inventing `active` from an unrevoked invitation. Keep the
original mutation UUID and request digest when reconciling a completed creation.

Before each write, call `plan --task-id <UUID> --input <absolute-plan.json>`. The plan contains the
step, SHA-256 of the complete tool request and the step's exact non-secret references. Use the returned
`mutationId` as that tool's idempotency key. Repeating the identical plan returns the same mutation ID;
a changed digest or reference is rejected. After a definite response, record the safe subset with
`finish`; after a timeout or unreadable response, use `mark` with `status:"uncertain"`; for a known
failure use `status:"failed"`. Keep the request body and UUID unchanged after an uncertain response.
Never record a one-time sharing secret in `finish`.

The sole changed-request exception is `replan` for a definite `preparePublication`
`PARTICIPATION_CONFIG_CONFLICT`. It appends the failed attempt to the same task journal instead of
overwriting it. It is unavailable for a timeout, uncertain result, or any other failed step.

For `saveDraft`, bind the complete request through `requestSha256` and record `projectId` plus
`expectedRevision` in references. Do not predict `sourceSha256` from the pretty-printed source file or
the template's canonical JSON digest: the service hashes its parsed source with `JSON.stringify` in
the service's key order. Treat the save response's `sourceSha256` as authoritative. Older plans may
already contain a different predicted hash. In that case read the exact saved revision back from the
service and pass its matching `projectId`, `revisionId`, numeric `revision` and `sourceSha256` as
`readback` in `finish`; the journal accepts this one normalization difference and retains both values.
Never save a new revision or change the original request to repair a journal-only hash mismatch.

At the start of a new conversation, run `show` and `next`, resolve the same account, and verify the
fixed project plus current server state. A succeeded step is not executed again. For an uncertain step,
compare the stored receipt references with a safe read, then retry only the identical request with its
stored mutation ID. Current project creation and visibility tools require that mutation ID; visibility
also binds the previously read `expectedRowVersion` and `expectedVisibility`. Keep all of them unchanged
on retry. If an older discovered schema lacks these fields, read and resolve the exact project before
retrying and do not retry while the outcome remains ambiguous. `pause` preserves the same task and
receipts while blocking further writes until verified recovery; `cancel` makes an abandoned task
read-only only when no cloud write remains unresolved. An unresolved write includes a planned request
whose client response was lost, so use `pause` even if `mark` could not run before interruption. If an
older journal was already canceled with an unresolved write, `recover` returns it to `paused` while
retaining the original request and mutation ID; verify the account and server state before `resume`.
Neither command revokes access or unpublishes anything.

Use one task journal for one fixed publication/update intent. A later update to the same project starts
a new task ID so it can retain a new draft/config/release chain without overwriting old receipts.
Before a new activation plan, the local CLI checks all task journals in its private state directory
under an activation-plan lock. If the same project and publication already have an activation journal,
inspect that task ID with `show` and `next`, reconcile its server result, and continue with its original
request and mutation ID. A second task ID is appropriate for a later, distinct publication, not for
retrying an ambiguous activation. If the plan lock is busy, retry the plan without changing its input.

## Choose the compatible path

Use the private draft pipeline for every new Page and Slides publication, including ordinary
self-contained HTML Pages. Save the fixed source, prepare it for the server-owned structural check,
then activate it when the user has requested publishing. This keeps the revision and exact audience
bytes available for reconciliation. The older `onimi_publish_html` tool is a legacy compatibility
path; do not choose it for a new Creator or Publish task. If continuing an uncertain older call made
through that tool, reconcile its original UUID, HTML, filename and notes with the server before any
retry. If its discovered input schema lacks `idempotencyKey`, do not automatically retry.

The private draft pipeline covers:

- `{kind:"page",html}` with a protocol manifest;
- `{kind:"slides",document:<validated Bento JSON>}`;
- controlled-cloud data; or
- any work that needs private revisions, a structural check and explicit activation.

Never export private author JSON, notes, hidden slides, manifests or premium template source through
`onimi_publish_html`. Onimi's Web editor remains the original Bento canvas with cloud actions in its
floating action control; the Skill does not create a replacement editor or hosted generator.
The anonymous Slides demo is ephemeral and has no save, review or publish authority. Move actual cloud
work to an authenticated project; never report demo state as a draft or release.

## Save and recover private drafts

1. Call `onimi_get_draft` (`draft:read`) for the current head.
2. For a local Page file, prefer the Creator's `draft-payload.mjs` upload flow through
   `onimi_begin_draft_upload` (`draft:write`). It uses one UUID, the head's numeric revision,
   SHA-256 and byte count of the exact private `{source,manifest}` JSON body, then sends that file
   with the short-lived upload capability. For Slides or an exact inline Page source, call
   `onimi_save_draft` (`draft:write`) with one UUID and exactly
   `{projectId, expectedRevision, source, manifest}`.
3. Record the response `revisionId`, `revision` and `sourceSha256`. Saving does not publish.

For a local Page file, use the Creator helper to prepare the upload body and begin request, then verify
the exact saved revision in `onimi_list_draft_revisions`. The begin tool grants a short-lived capability for this body; its response
belongs in a private local file and must never be printed with source or credentials. The helper sends
the file bytes without reading the Agent's OAuth credentials. A local checksum or an `INVALID_SOURCE`
response to fabricated input is not a save receipt. Do not create another project to bypass a failed
save. Finish `saveDraft` in the task journal only after the server revision/hash/manifest and local
body match.

For a transport failure, timeout, 5xx or unreadable success response, keep the exact UUID and body for
retry. A definite conflict means read the new head and reconcile; never change `expectedRevision` while
reusing the old UUID.

Use `onimi_list_draft_revisions` for history. Restoration is explicit and append-only: fetch the chosen
revision with `onimi_get_draft`, separately fetch the current head, then save the chosen `source` and
`manifest` with the current numeric revision and a new UUID. This creates a revision and does not
rewrite history. Warn about unsaved local edits before leaving a live editor.

## Configure controlled data only by choice

For a selected controlled-data workflow, keep both choices explicit: collection `recordScope`
(`shared` for one group record, `participant` for isolated personal records) and share
`identityMode` (`nickname` or `account`). The trusted FAB asks for a nickname or takes the user
through login before saving. Account-required is not identity verification. Return the grant's
`redeemPath` privately to the owner as the participant entry, together with the owner dashboard URL.
Before creating a new grant, read the current participation configuration and project policy epoch;
send their observed `latestVersion` and `policyEpoch` as `expectedConfigVersion` and
`expectedPolicyEpoch`. On a conflict, show the new settings for owner review and start a new request;
for a timeout or uncertain response, retry only with the same key and exact body.
The ordinary audience URL alone does not establish a participant session. After publishing, verify
server-acknowledged saving and reload from a second authorized session; a changing URL or successful
draft save is not proof of collaboration. A successful form save is recorded without author review.
If publication status reads return a legacy `pending-review` record, report its actual status and
reconcile it before activation.

If the requested interaction could either stay in this browser or collect/share data across people or
devices, explicitly ask the user to choose local interaction or controlled sharing unless that choice
is already clear. If the manifest uses `controlled-cloud`, follow the Creator Skill's
`controlled-data.md`. Confirm real sharing was explicitly selected and the project is `private`. If the
user also requested public or unlisted access, stop and ask them to choose public/unlisted local content
or private controlled sharing; do not silently downgrade either request. Read
`onimi_get_participation`, then call `onimi_configure_participation` with the current `latestVersion`,
exact mode, identity policy, owner visibility and manifest (`collectionKey`, `batchKey`, `formVersion`,
questions), plus the task journal's UUID. Persist the returned configuration `id`, `version` and
`manifestSha256`; this hash covers the manifest only, not the mode, identity policy or owner
visibility. Do not persist the manifest. Use `onimi_set_participation_lifecycle` only for an explicit
pause/resume/external-access management action and preserve its receipt separately. A candidate
configuration does not revoke existing sessions and does not become the active publication
configuration merely because it was saved. If these versioned participation tools are absent, do not
fall back to legacy `onimi_configure_collaboration` for a new ordinary workflow or claim version
binding; preserve the task and point to the dashboard. A conflict requires another owner-state read and
reconciliation. Never switch controlled data to `public` or `unlisted`, and never use legacy HTML
publishing to bypass configuration, server publication checks or access grants.

If a configuration save loses its client response, inspect the original journal and call
`onimi_get_participation_receipt` with that project's original mutation UUID. Its owner-scoped result
identifies the exact accepted configuration even when a later version is active. Compare its mutation,
configuration ID/version, server manifest hash and the full `onimi_get_participation` history before
finishing the original operation; a current latest version alone is insufficient. An absent receipt
does not prove the write was canceled. Preserve the original request and key, and do not create a new
configuration while its result is uncertain. The service may normalize question text before hashing,
so a local predicted manifest hash can differ. `task-state.mjs finish` permits that difference only
with a previously succeeded journal for the same mutation and complete local request digest, plus the
exact server mutation/configuration readback; keep both hashes and the original plan. If the sibling or
readback is missing, stop for reconciliation instead of rewriting the plan or inventing a success.

The participation manifest is **different** from the HTML's `onimi-artifact` manifest. Send its
complete wrapper, not a collection by itself. Every question needs `id`, `fieldKey`, `label`,
`meaning`, `type` and `required`; `options` is allowed only for bounded string choices. Do not send
`maxLength` on a participation question; length limits belong to the artifact field and form UI.
For a two-question, independent response form, the `manifest` argument is shaped like this:

```json
{
  "schemaVersion": 1,
  "collections": [{
    "collectionKey": "responses",
    "batchKey": "round_a",
    "formVersion": 1,
    "questions": [
      {"id":"attend","fieldKey":"attend","label":"Will attend","meaning":"Whether the participant will attend","type":"boolean","required":true},
      {"id":"topic","fieldKey":"topic","label":"Discussion topic","meaning":"Topic the participant wants to discuss","type":"string","required":true}
    ]
  }]
}
```

Validate this shape before planning the external write. If a request is definitively rejected as
`INVALID_INPUT`, do not replay its UUID with changed parameters. Read the latest configuration,
correct the request, and plan a new mutation with a fresh UUID against the same selected project.

## Check the fixed revision, then publish explicitly

Before preparing publication, use the current Agent model to review the exact saved audience content
under the Creator module's [content preflight](../onimi-pages-creator/references/content-preflight.md).
If that module is unavailable, apply the same categories here: pornography, gambling and fraud are
prohibited; a political topic alone is not prohibited, and an explicit applicable sensitive-content
rule needs a known scope. Timezone does not verify location. Stop on a clear violation, ask for the
smallest necessary clarification on uncertainty, and never invent a pass. This is an Agent check and
is not an Onimi platform semantic safety certification. No extra local model installation is needed.

Read the fixed saved draft and call `onimi_list_publications` (`release:read`). It returns the current
`policyEpoch`, `activeReleaseId` and publication records, but never author source.

Create one immutable preparation transaction for `onimi_prepare_publication` (`release:publish`):

```json
{
  "projectId": "<project UUID>",
  "sourceDraftRevisionId": "<saved revision UUID>",
  "sourceSha256": "<saved source SHA-256>",
  "expectedPolicyEpoch": 1,
  "expectedActiveReleaseId": null,
  "participationConfigVersion": 3,
  "idempotencyKey": "<UUID>"
}
```

Omit `participationConfigVersion` only for an artifact with no participation configuration. Use the
exact saved candidate version for a controlled-data publication; never substitute “latest.” Use the
actual current active release UUID instead of `null` when one exists. Keep this complete body and UUID
unchanged after an uncertain response; do not re-read the head and silently submit different bytes.
The accepted HTTP response uses `202` semantics because preparation and activation are separate.
The server checks the immutable staged audience for structure, permissions and dangerous document
loading and normally returns `approved`; it does not run a semantic model or activate the release.
If the structural check fails or the result is uncertain, do not call activation. Keep the same
request UUID/body for reconciliation; do not claim publication succeeded. The current active version
is unchanged until explicit activation.

If prepare returns a definite `PARTICIPATION_CONFIG_CONFLICT`, stop that publication attempt. Keep its
project, fixed draft revision/hash, configuration version and request UUID in the task journal; do not
retry the rejected body with a substituted version or silently create another project or release. Read
`onimi_get_participation` and `onimi_list_publications` again. Explain which participation rules changed,
which version is merely a candidate and which version is active. Reuse a choice the owner already made;
ask only if a decision about the changed rules is still unresolved. Check that the original rejected
attempt created no publication: compare the complete `onimi_list_publications` result from before and
after, following `nextCursor` until exhausted rather than counting only the first 20 records. Mark the
old `preparePublication` operation `failed` with code
`PARTICIPATION_CONFIG_CONFLICT` and `retryable:false`. Once publication under the new rules is
authorized, verify the same saved artifact still matches the current manifest. Use `replan` with the
old `supersedesMutationId`, a **new** UUID, the SHA-256 of the **new complete request**, and exact
references for the same project, saved revision/hash, policy epoch and active release but the confirmed
newer `participationConfigVersion`. Its `readback` must record the current latest config version,
current active release ID, and complete publication counts before and after the rejected attempt.
Use `onimi_get_participation.latest.version` for `readback.latestConfigVersion` and
`onimi_list_publications.current.activeReleaseId` for `readback.activeReleaseId`; count every
`publications` page for `publicationCountBefore` and `publicationCountAfter`.
Replan rejects
changed project/source/policy/active release, a reused UUID, or a changed publication count; reconcile
those cases separately. Call `onimi_prepare_publication` only with the UUID/body returned by the
successful replan. The journal retains every rejected attempt and `next` points to the new one.
An idempotent replay of a previously accepted prepare is its original result, not renewed approval for
changed rules; never treat it as a fresh successful structural check.

Read back with `onimi_list_publications`; status reads are safe and do not resubmit. A legacy
`pending-review` record is not newly approved by this workflow; reconcile its exact source and
check status before continuing. `processing` and `staged` are incomplete; `rejected`, `failed`,
`historical`, and `superseded` are not publishable. Only the latest record with an approved server
check, the current policy epoch and the current active-release expectation can be activated.

After the server check passes, call `onimi_activate_publication` only when the user has explicitly requested publishing.
A clear initial “publish” instruction remains authorization after the structural check; a request to create, save or
preview does not. Use a fresh UUID with exact
`{projectId, publicationId, expectedActiveReleaseId}`. Retry uncertainty with the same UUID/body. On a
conflict, re-read publication state and show what changed; do not blindly substitute the new active
release or policy epoch. A `PARTICIPATION_CONFIG_CONFLICT` at activation means the reviewed candidate
cannot go live under the newer rules. Re-read participation state and leave the current live release
untouched; only a newly confirmed, separately checked publication may use the newer configuration.
Report success only when the target becomes `active`.

## Apply access and return the result

For local-data projects, preserve current visibility on an update unless the user explicitly asks to
change it; apply the confirmed access for a new project. If `onimi_set_visibility` is available, map
explicit public/listed intent to `public`, link-only intent to `unlisted`, and removal of audience
access to `private`. Read the current project first, then journal and pass its `rowVersion` as
`expectedRowVersion`, its current access as `expectedVisibility`, and the journal UUID as
`idempotencyKey`. Keep those fields and the requested visibility identical on an uncertain retry.
Narrowing an existing project to private can happen before publication.
Widening access should happen only after the requested release becomes active, so an older active
release is not exposed as the new result. If the tool is unavailable, keep the actual visibility and
report that the requested change was not completed. A private URL is not a public sharing result.
Controlled-cloud projects always remain private and use invitations, codes or scoped links.

After activation, re-read `onimi_list_projects` and use the active project's `audienceUrl` for the
stable viewing link. Never derive a URL from a slug or confuse `editorUrl` with a viewer link. A
private URL still requires an authorized viewer and is not a public sharing result. Return the stable
URL, version URL when supplied, version/publication status and actual access. A failed or pending
release does not replace the current page.

## Support and stopping conditions

- `insufficient_scope`: keep local work and use the host's reconnect/consent flow. Never approve consent
  for the user.
- Unknown mutation result: read the current draft or publications first, then retry only the retained
  identical transaction. Do not generate a new UUID to make progress.
- Definite HTTP 400 or 403, or a 409 conflict: preserve the error code, project, fixed revision/hash and
  failed stage. Resolve input, authorization or conflict. Dashboard upload does not bypass the same
  storage or authorization boundary.
- Missing new tools: preserve the artifact and use `https://onimi.ai/dashboard` as the no-CLI fallback.
  Do not claim draft, Slides or controlled collaboration succeeded through old tools.
- Plan/storage/visit limit: relay it without deleting or replacing projects.

## Check for updates

Do not interrupt publishing to check. The bundled manager applies only to a direct-download installation
with `.onimi-skill.json`. Resolve this Skill's directory and use `scripts/manage.mjs status` offline or
`check` at most daily. Never update automatically. After explicit approval of an exact version, run
`scripts/manage.mjs update --confirm onimi-pages-publish@<version>`. npm, GitHub, ClawHub and host-managed
installations use their own update flow.
