# Human Writing for DeepSeek Harness

<p align="center"><img src="../../assets/logo.png" width="280" alt="Human Writing: fountain-pen handwriting and terminal code"></p>

> Make AI-assisted writing more natural with multilingual editing, chunked long-form collaboration, and continuity review.

A DSH/Cordis plugin for novels, papers, reports, essays, and supplied-draft cleanup.
It contributes a compact writing protocol before generation and mounts local tools
for genre-aware prompt compilation, lint, factual fidelity, voice preservation,
and bounded long-form review. The existing DSH agent writes the prose; this plugin
does not make a separate model call or promise authorship-detector scores. A host
with native delegation can assign writing roles to its own subagents.

## Install

Requires Python 3.9+ on PATH and a DSH profile with tools and systemPrompt services.
No pip installation of human-writing-skills is needed: the release bundles its Python
core and Markdown modules. Use Node ^22.19.0 or >=24.0.0 as required by current DSH.
Integration-tested with official DSH 0.2.1-rc.2 and 0.2.2-rc.3 packages. Peer ranges also admit
0.2.0-rc.2 and the 0.2.1 alpha line; those other versions have not been tested here.

```powershell
dsh plugin --profile web add https://github.com/whh110112/human-writing-skills/releases/download/dsh-v0.3.1/dsh-advanced-human-writing.tgz
```

For the desktop profile, replace `web` with `desktop`. Restart the affected profile.
If Python is not named `python`, set `PYTHON` to its executable path before starting DSH.
Alternatively, install the complete repository root at a pinned tag:

```powershell
dsh plugin --profile web add github:whh110112/human-writing-skills#dsh-v0.3.1
```

The npm package manifest lives at the repository root. The adapter subfolder is
private and is not a standalone npm package. No npm publication is claimed.

## Use In DSH

- Novel: “Use Human Writing to continue the scene in Chinese. Preserve the supplied
  character ledger and let both speakers respond; avoid a reflective tail.”
- Paper: “Write the results section from these observations. Preserve uncertainty;
  do not invent citations, statistics, or significance tests.”
- Report: “Write the weekly report with current status, blockers, owners, and next steps.
  Keep planned work separate from completed work.”
- Rewrite: “Polish this draft while preserving my voice, meaning, and useful ambiguity.”
- Advice: “Diagnose this article without rewriting it.”

The model receives the plugin's conditional guidance only for authored writing,
rewriting, or review. It is instructed to call `mcp__human-writing__compile_generation_prompt`
before substantive generation, apply the returned genre protocol, and use lint and
fidelity tools before delivery where relevant. These remain model-followed instructions,
not a guarantee that a model will follow every rule. Deep audits load only on demand.

Use workspace-relative `source_paths` for factual evidence and `reference_paths`
for voice samples; both are restricted to the configured root. They are distinct.
The compiler will not borrow facts from a voice sample. See runnable input examples
in [examples](examples) and a [keyless integration demo](DEMO.md).

## Long-Form Writing

For requested output of at least 10,000 characters or words, or an explicit
multi-agent long-form request, the prompt routes to
`writing__human-writing__longform_guidance`. This local tool loads the detailed
protocol on demand; ordinary writing and long-input reviews do not trigger it.
Its name follows `serverName`. `generationGuidance: false` removes the prompt
section but retains this tool and the MCP tools.

Example request: "Use multiple agents to write 20,000 words from outline.md;
save the reviewed manuscript to manuscript.md." Save an agreed outline first,
then call `mcp__human-writing__plan_long_form_writing` using
[longform.json](examples/longform.json). Length refers to requested output, not
outline length; `length_unit` distinguishes words from characters.

The host lists ready tasks and claims each with an explicit `agent_id`. Claims
provide the complete role-specific prompt and submission schema; forward both
unchanged. Roles run in this order: outline checker, chunk planner, writer per
chunk, separate editor per chunk, final continuity reviewer, assembly. Preserve
the claimed identity when submitting the actual structured `result` object with
`submit_writing_result`. Re-list readiness after submissions. Revisions are
bounded, approvals gate successors, and exhausted revisions must be reported.
Task IDs are `outline-check`, `chunk-plan`, `write-0001` / `review-0001` pairs,
then `continuity`. Claim fields are `content` and `result_schema`. Each editor
must differ from its writer; the final reviewer must differ from all writers.
Claims also return `claim_token`, copied into `result_schema.claim_token`. Forward
the full prompt, full result schema, and token unchanged. The role must copy the
current token into `result.claim_token`; track it alongside child ID, task ID,
and `agent_id`. Active same-agent resumes retain the token; reclaim/revision
attempts receive a new one. Discard stale child results from earlier attempts,
never relabel old results with the new token or submit them to the new attempt.
In sequential mode the next writer waits for the previous editor's approval.
Only `execution_mode: "contract"` permits parallel ready tasks, with approved
independent block entry/exit contracts, bounded by `max_parallel` and host limits.
`max_parallel` limits simultaneous claims. A 60,000-unit target with 5,000-unit
chunks creates twelve writing jobs plus review jobs, not twelve guaranteed
concurrent agent processes. Contract dependencies still gate readiness.
Default sequential mode remains sequential even on a parallel-capable host.
Call `verify_writing_project` successfully before `assemble_writing_project`.

### Native DSH Delegation

The official `@deepseek-ai/dsh-subagent` and `@deepseek-ai/dsh-tool-subagent`
0.2.1-rc.2 package documentation and shipped implementation establish this
host composition (configure it in the host, not in this writing bundle):

```yaml
- name: '@deepseek-ai/dsh-subagent'
- name: '@deepseek-ai/dsh-subagent-spawn-in-process'
- name: '@deepseek-ai/dsh-tool-subagent'
  config:
    provider: spawn
    toolName: subagent
```

The normal host agent driver/model configuration is still required. The native
tool accepts `description` and `prompt`; use its advertised schema if configured
under a different name. It returns a child ID immediately, not the final result.
Map that ID to the task's claimed identity, await the runtime completion notice,
then submit the child's structured result unchanged. A fresh child need not see
the parent conversation. This adapter neither installs nor configures a provider
and does not bypass host permissions, capacity, or depth limits.

The lower-level `ctx.agents.create()` API also requires a registered agent driver;
an agent registry or MCP alone cannot delegate. If no usable runner exists,
disclose this and execute sequential distinct role passes, labeling identities as
role passes rather than independent agents. Writer/editor passes remain separate;
do not claim concurrent agents, silently reassign claims, or fabricate approvals.

The checked-in keyless tests use actual Cordis/MCP without a driver or subagent
provider. They verify the route, real writing-tool schemas, tools-only mode, and
unload behavior, not native child execution or model adherence. Actual delegation
requires the host composition above and its configured model.
The real MCP smoke test also plans two chunks, checks outline approval gating,
claims the full prompt/schema, rejects a mismatched submission identity, submits
an outline receipt, and confirms incomplete work cannot be assembled.
It also checks token preservation on active resume, missing/stale-token rejection,
and a new token after a real editor-requested writer revision. Late output from
the first writer attempt cannot complete the new claim.

## Configuration

For agent mode, call `writing__human-writing__agent_capabilities` before delegation.
It returns the configured tool's caller-scoped visibility and parameter schema.
Set `delegationToolName` when the host uses a name other than `subagent`. Discovery
is live on each call, including after provider reloads; it never starts an agent,
installs a provider, bypasses a scope restriction, or changes models/presets.
The full long-form protocol is still loaded only on demand. Claims expose their
lease; oversized assignments are paginated and expired claims are clearly marked.
Review schemas include source checks for serious prose, not fiction.

The supplied patch mounts the plugin as `advanced-human-writing-mcp`.

| Field | Default | Purpose |
| --- | --- | --- |
| root | DSH launch working directory | Allowed writing workspace |
| pythonCommand | PYTHON or python | Python executable, not a shell command |
| serverName | human-writing | MCP namespace; tool and guidance names follow it |
| generationGuidance | true | Set false to keep tools without the prompt section |
| toolCallTimeoutMs | 60000 | Individual tool timeout |

Config `root` explicitly when DSH is launched outside the writing project. Python
starts in isolated mode and loads the bundled core before workspace modules.

## Permissions And Distribution

The plugin starts a local Python stdio process. The local core reads supplied text
and workspace files, and writes review packages only through invoked planning/report
tools. It does not install Python packages, open a network listener, upload drafts,
or publish generated writing. DSH's configured model receives the text used in its
normal conversation and calls; its existing provider/privacy settings still apply.
External publication of a manuscript requires the user's instruction to DSH.

Category: Skills / Tools & Capabilities. License: MIT. This is a community plugin,
not an official DeepSeek product. Market submission and maintainer acceptance are
separate from publishing an installable release.

## Development

From the repository root:

```powershell
pnpm install --frozen-lockfile
pnpm test
python -m unittest discover -s tests -q
pnpm pack --pack-destination dist
```

Tests negotiate with the real bundled server, compile fiction/paper/report prompts,
verify facts, reject path escapes, and mount/call/unload through official Cordis and
MCP packages without any model/API key. They verify integration, not literary quality.
