# Multi-Agent Long-Form Writing

## When To Load

Use when the user requests a long new manuscript, continuation, or substantial
multi-section document, typically 10,000 or more output characters/words, or asks
for multiple writing agents. For reviewing an existing manuscript, use the
established chunk-audit workflow instead. Do not load this protocol for a short
answer merely because its source material is long.

## Execute The Five Roles

1. **Outline checker:** validate the agreed outline and canonical context before
   allocation. Identify contradictions, missing prerequisites and unsupported
   claims. A missing outline requires a proposed outline first; do not present
   invented facts or settings as supplied authority.
2. **Chunk planner:** allocate explicit units and targets, cover every outline ID,
   and define each block's purpose, entry state and exit state. Preserve one
   shared language/voice contract. Planning labels need not appear in the prose.
3. **Writers:** each receives its claim's complete prompt and schema, the assigned
   outline units, approved predecessor state, relevant evidence and optional voice
   references. Write full prose, not a synopsis. Carry established fact keys and
   pending exchanges forward; changes need literal transition evidence.
4. **Independent editors:** review every paragraph of each actual writer result
   against its outline, voice, continuity and naturalness. Cite specific evidence;
   use the existing focused genre modules rather than loading all skills. For
   serious texts verify evidence and uncertainty; for narratives inspect physical
   transitions, interpersonal responses and earned endings. A pattern score is an
   editing lead, not proof of quality or authorship. Return local revision requests
   when needed, preserving useful ambiguity and purposeful repetition.
5. **Main continuity editor:** after all blocks pass, inspect every adjacent pair,
   the accumulated states, unresolved threads and shared style. Read stored bodies
   for claims that the boundary excerpts cannot support. Approve assembly only
   after all required chunks and boundaries have current receipts.

## Coordinate Through Tools

Call `plan_long_form_writing` with the saved outline, output directory, style,
target length and unit; default block target is 5000 non-whitespace Unicode
characters. `length_unit: words` instead counts whitespace-language word tokens.
60,000 / 5,000 creates twelve writer assignments and twelve editorial assignments,
plus the outline, planning and continuity tasks. It does not imply twelve agents
can run concurrently.

Use `list_writing_tasks`, `claim_writing_task` and `submit_writing_result`. Forward
the returned `content` and `result_schema` unchanged to a native host subagent;
submit the actual result under the same stable `agent_id`. A start acknowledgement
is not a completed result. Echo the current `claim_token` in the result so an old
worker cannot submit into a revised assignment. Writers and their editors must have distinct identities.
The final editor must differ from every writer.

In DSH, inspect the caller's delegation schema with the plugin's on-demand
`writing__human-writing__agent_capabilities` tool (use the configured namespace).
A visible tool is not proof of provider readiness. Respect its advertised
parameters, permissions, depth and model/preset authorization; do not change the
user's model route merely to run this workflow.
If a claim returns a file pointer, read its entire assignment using paginated
`read_project_context` calls, not a summary. Claims expose `lease_seconds`;
renew with the same task and identity before expiry if its child is still running.
After expiry or reissue, never retag old child output for a fresh attempt.

The default `sequential` mode releases a writer after the previous block's editor
approves it. Use `execution_mode: contract` only for explicitly approved parallel
writing with declared independent entry/exit contracts and earlier-block dependencies.
Limit active claims to host capacity and `max_parallel` (default four). Reviews of
independent blocks can proceed as those blocks become ready. Do not parallelize a
dependent scene by guessing what another writer will produce.

Revision feedback reopens affected writers and invalidates downstream approvals.
Two revision rounds per affected block are permitted; an exhausted budget requires
corrected inputs or a revised brief in a new package, not a fabricated approval.
Snapshots and prior results remain inspectable. After interruption, list and resume
the package; do not recreate completed work or overwrite state files.
Incoming pending threads must remain listed or have quoted resolution evidence.
Conflicting states from parallel branches require explicit reconciliation evidence;
never select one branch's value silently.

Call `verify_writing_project`, then `assemble_writing_project` after it passes.
For CLI-only hosts the equivalent commands are `plan-writing`, `writing-tasks`,
`claim-writing`, `submit-writing`, `verify-writing` and `assemble-writing`.

The host supplies the model and agent runner. If native delegation is unavailable,
state that limitation and use sequential role passes with honest role-pass IDs;
do not describe them as independent agents. If no local tool runtime is available,
use the same per-block artifacts through host file tools and explicitly identify
that receipt validation is manual. Do not claim the programmatic gates ran.
