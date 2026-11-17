# Writing Long Documents With Multiple Agents

Use this workflow to create long prose from an agreed outline. Existing-manuscript
review remains `chunk-audit`; it does not generate replacement chapters by default.
The core stores dependencies, snapshots, drafts and review receipts. Your host's
model and native agent tools perform the writing and editorial judgments.

## Roles And Gates

| Role | Assignment | Gate |
| --- | --- | --- |
| Outline checker | Check every outline unit against canonical context and prerequisites. | Quote every unit; unresolved issues block planning. |
| Chunk planner | Allocate block targets, outline coverage, voice and state contracts. | Every outline unit belongs to at least one block; dependencies are acyclic. |
| Writer for each block | Produce full prose and a cumulative state handoff. | Length is 80–120% of the allocated target; established state keys cannot disappear. |
| Editor for each block | Independently check actual text for outline adherence, continuity, voice and AI-like filler. | Quote every paragraph; verify the current draft digest; all checks pass before approval. |
| Main continuity editor | Check every adjacent pair and overall coverage, state and voice. | Every chunk and boundary is covered before assembly. |

For research, reports and news, editors additionally check evidence, attribution,
numbers and uncertainty. Fiction response/scene rules remain conditional. Language
and tone come from the approved style contract and any explicit reference samples.
Factual sources and voice references are separate inputs.

## Plan A 60,000-Character Manuscript

```powershell
human-writing-skills plan-writing --outline outline.md --context ledger.md --style fiction --target-length 60000 --chunk-size 5000 --output-dir book-writing
human-writing-skills writing-tasks --package-dir book-writing
human-writing-skills claim-writing --package-dir book-writing --task-id outline-check --agent-id outline-checker
```

The plan contains twelve writing tasks, twelve editorial tasks and three shared
tasks. The first ready task is `outline-check`, followed by `chunk-plan`, the
`write-0001` / `review-0001` pairs, and finally `continuity`. The claim returns
`content` and `result_schema`; forward both to the assigned agent. Save its actual
JSON result, echoing the claim's `claim_token`, and submit it, then query readiness again:

```powershell
human-writing-skills submit-writing --package-dir book-writing --task-id outline-check --agent-id outline-checker --result outline-check-result.json
human-writing-skills writing-tasks --package-dir book-writing
human-writing-skills verify-writing --package-dir book-writing
human-writing-skills assemble-writing --package-dir book-writing --output manuscript.md
```

The last two commands succeed only after the required approvals. Assembly keeps
the planned block order and inserts paragraph separation, without manufacturing
chapter headings or rewriting the approved text. It requires a new output path.

`characters` counts non-whitespace Unicode characters, including punctuation;
`--length-unit words` counts word tokens and is suitable for languages written
with word boundaries. Neither is a token budget. A target of 60,000 words is much
larger than 60,000 Chinese characters. Adjust block size for model output limits;
do not use repeated sentences to meet the target.

## Serial And Parallel Writing

Default `--execution-mode sequential` waits for each preceding editor's approval
before handing its state and text ending to the next writer. This supports scenes
whose actions depend on earlier prose. Distinct writer/editor pairs can still be
different agents; sequential dependency does not mean one giant chat context.

Use `--execution-mode contract` only when parallel writing is explicitly requested
and a planner can attest to independent blocks. It requires entry/exit states and
either earlier chunk dependencies or an explicit `independent: true` declaration.
The queue enforces these declarations and `--max-parallel` (default four); semantic
independence is still an editorial judgment. Do not mark interdependent scenes
independent merely to start more agents. Twelve blocks need not be twelve concurrent
processes. Reports with independent sections are often easier to parallelize.

When a chunk is handed off, its `state` contains stable keys for established facts.
All incoming keys must remain. A changed value needs a `state_changes` record with
matching before/after values and an exact quotation from the new prose. This catches
unrecorded moves, ownership changes, and lost state entries; it does not prove that
the quoted event is physically or logically sound. Editors check that meaning.
If parallel predecessor branches disagree, `state_changes.before` must contain the
complete list of conflicting values and the new prose must evidence a resolution.
An incoming pending thread must remain pending or appear in `resolved_threads`
with an exact quote showing its resolution; it cannot silently disappear.

## Revisions, Resumption And Large Contexts

An editor's `revise` response includes evidence and a proposed local correction.
It reopens the affected writer and invalidates every dependent draft/approval,
including final continuity. Independent branches can retain their approvals. Two
revision rounds are allowed per affected block; further requests block that block
until the brief or inputs are corrected in a new package. An outline that fails
its initial check similarly requires corrected inputs, not automatic invention.

Claims are owned by stable agent IDs. A second agent cannot take an active claim;
the owner can resume it. Claims expire after an hour, allowing interrupted jobs to
be reclaimed. A current `claim_token` is required with every result; expired claims
and late results from older attempts are rejected. Feedback is read from its stored
report path rather than copied wholesale into each revision prompt.
Submitted results are versioned and hashed; changed snapshots or
result files cannot reuse the old approval. Never edit package JSON to bypass a gate.

The final reviewer reads `continuity-index.json`, containing block digests, entry/
exit contracts, actual state, pending threads and boundary excerpts. Use
`read_project_context` with `offset` and `next_offset` until `next_offset` is null;
read the referenced draft-result files for claims not supported by the excerpts.
This keeps the full manuscript out of each prompt. Role prompts have a
60,000-character limit. A block review exceeding that limit is saved as a complete
paged assignment; the reviewer must read all pages and return every paragraph receipt.
Other oversized context fails explicitly, and results retain transport limits.
Use compact canonical ledgers and split a very large work into volumes
when a role's context or result exceeds the limit. Sources and references are only
loaded for the blocks to which the planner assigns their IDs.

## MCP And DSH

The MCP equivalents are `plan_long_form_writing`, `list_writing_tasks`,
`claim_writing_task`, `submit_writing_result`, `verify_writing_project` and
`assemble_writing_project`. Inputs and output paths stay within the configured root.

In DSH, request a long output or explicitly ask for multi-agent writing. The plugin
loads its detailed protocol through `writing__human-writing__longform_guidance`
only on demand; the name follows a custom `serverName`. It uses a host-provided
native delegation tool when configured. For actual parallel subagents, DSH needs
its subagent service, provider, tool and model driver; MCP alone does not start
processes. See the [DSH guide](../plugins/deepseek-harness/README.md).

Without a native runner, sequential role passes remain available but must be
described as role passes, not independent agents. Unit and integration tests verify
coordination, storage and gates; they do not establish literary quality or guarantee
an AI detector score.
