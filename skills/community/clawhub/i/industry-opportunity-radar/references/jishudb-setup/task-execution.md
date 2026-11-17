<!-- Generated from templates/task-execution.md; do not edit this copy. -->

# Task execution defaults

Use this contract for task scope, existing authorization, and bounded recovery.
It does not grant account access, installation, publication, or new write scope.

## Required JishuDB setup precedes task work

Missing host tools and an empty MCP configuration trigger the packaged
routine setup guide (`references/jishudb-setup/references/setup-quickstart.md`
relative to the calling task Skill), just as a failed connection
does. Read it immediately; follow its single discovery pass and helper commands, then
client/runtime verification. Do not wait for a callable MCP tool or ask the user
to arrange setup independently. Reuse authorized scope and preserve required
installation authorization, OAuth, agreement, and OS user-presence gates.
Read-only discovery and planning need no extra confirmation. Reuse a user's
explicit setup authorization for the matching transaction; ask only for missing
or changed scope. Present a short action summary, not plan JSON/hash tables or
an A/B prerequisite menu. Keep bounded download, verification and client setup
moving until a real user action or a specific failure blocks the next step.

Keep public research, source transfer, drafting, and rendering pending until
required JishuDB readiness, destination, and write scope pass. Put this
prerequisite first in any task list. Return `USER_ACTION_REQUIRED` or `BLOCKED`
with the concrete next action if setup cannot proceed. Do not replace required
JishuDB persistence with local files or promise optional later archival.

## Start without an intake form

- The user's explicit count, format, language, and constraints override every
  default and example in the calling Skill. Produce only the requested outputs.
  Defaults fill omissions; they are not a checklist to ask the user to approve.
- Resolve routine audience, style, dimensions, filenames, and local output
  directory yourself. Use a new run subdirectory in the host workspace unless
  the user chose another location. State material assumptions briefly and work.
- Reuse the selected service, verified KB ID, and existing consent for the same
  material and purpose. A working write-capable connector proves capability,
  not consent to put unrelated data in an arbitrary KB. If destination or
  retention authority is unresolved, propose one concrete destination and ask
  once for only the missing scope; do not ask for IDs, profile names, UUIDs,
  revision settings, or an output directory. Reuse the answer throughout the run.
- Request required write scope in the initial OAuth flow when not already
  granted. Do not reauthorize after a successful grant just because a later
  step says "obtain approval". Changed scope and OS/browser consent still
  require the appropriate user action. Installation follows its own contract.
- Optional preferences, additional variants, and personal-practice retention
  must not block the requested deliverable. Personal retention stays off unless
  explicitly requested and consented; do not offer it as a mandatory question.

## Use working tools, with an exit from failures

- Use the host's loaded authenticated MCP tools first. A successful real call
  is stronger evidence than an unauthenticated curl probe. Do not repeatedly
  inspect configuration or raw endpoints when the host connection works.
- Inspect the live schema or documented CLI help and run one minimal output
  probe before investing in a generator. Allow at most three discovery/probe
  calls or two minutes, whichever comes first, per route. Do not reverse-engineer
  installed bundles, guess undocumented DSLs, or start a new toolchain merely
  to finish content. Switch once to a known available fallback; otherwise
  report the missing capability and preserve useful output. These fallback
  rules apply to output tools, never to required JishuDB setup or persistence.
- For a transient read/render failure, retry once, respecting Retry-After, then
  use the fallback or report the gap. Authentication, permission, unsupported
  format, and invalid-input failures require their specific recovery, not a
  delay loop. Inspect structured result status even if a process exits zero.
- For uncertain writes, reconcile the existing ID/job first using the calling
  Skill's persistence procedure. Never repeat an upload or rotate an identity
  just to escape a timeout. Reuse authorization for the unchanged repair scope;
  a new destination, material, installation, or paid service is a new scope.
- Inspect each final artifact once and allow at most two focused correction
  passes for observed defects. Compare the actual file/version once if a
  preview seems stale; do not loop through renamed copies or speculative
  cache fixes. Stop with the remaining defect identified if still unresolved.
- Finish when the requested artifacts, required records, and checks are done.
  Do not add more outputs or cosmetic passes. While working, give brief progress
  at stage changes or after about a minute without visible results. A blocked
  export or persistence step must not hide already-created files: return PARTIAL
  with their paths, missing checks, and the specific recovery action. This
  covers a later failure after readiness passed; it does not authorize new
  content generation while initial JishuDB setup is blocked.

## Keep evidence and persistence proportional

- Read only references, tool outputs, source sections, and image previews needed
  for the current step. Avoid dumping bundled code, full logs, or large repeated
  tool results into the conversation. Keep durable paths/IDs for continuation.
- Start research with the smallest source set that supports the requested
  result, then one targeted gap pass. Search counts and reading-list sizes are
  ceilings, not quotas. Expand for an explicit deep-research scope or a concrete
  unresolved claim, not to fill a template.
- Keep all required source, draft, final, and revision information, but combine
  related sections into a small number of size-bounded Notes when allowed by the
  live contract. A record category need not become a separate Note or import.
  Preserve actual draft/final versions and source coverage; do not import every
  discovered URL when a permitted excerpt/source card is sufficient.
- Poll existing jobs within the calling Skill's limits, honoring server delay
  hints. At the budget limit, return pending IDs and PARTIAL; do not ask the user
  to keep extending waits or report queued work as complete.
