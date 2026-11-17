# Keyless Integration Demo

This is a prompt/tool integration demonstration, not a model-generated manuscript.
Run `pnpm test` from the repository root with Python 3.9+ available.

The official Cordis test mounts SystemPrompt, ToolRuntime, and this plugin, then
discovers `mcp__writing-integration__compile_generation_prompt`, calls it with
an academic-writing task, checks that the returned instructions include the
generation-quality protocol, and unloads the plugin. Both tools and prompt section
are removed. The protocol test additionally uses a real Python stdio process to:

1. Negotiate MCP and list tools.
2. Compile fiction, academic-paper, and formal-document instructions.
3. Supply a source file containing an observed six-hour device test.
4. Confirm that the evidence appears in the self-media writing prompt.
5. Reject `../outside.md` as a source path.
6. Compare “The effect may be 20%.” with “The effect is 20%.” and receive
   `needs-review`, even though the number remains unchanged.

The test places a fake `humanwriting.py` in the workspace; isolated startup still
loads the bundled core. These checks require no DSH account or LLM API key.
Human/native-speaker evaluation of the prose is a separate activity.

## Long-Form Route

The Cordis test also checks that a >=10,000 requested output / explicit multi-agent
request is routed to `writing__writing-integration__longform_guidance`. The detailed
protocol is absent from the initial prompt and is returned by executing that tool
through the real DSH tool runtime. It explains unchanged claim prompt/schema
forwarding, stable claim identity, separate writer/editor roles, bounded revisions,
approval dependencies, contract-only parallelism, verification, and assembly.

The same test discovers all six writing tools from the real Python MCP process
and checks the length-unit, execution-mode, structured-result, and identity schemas.
Tools-only mode still exposes the on-demand protocol; plugin unload removes it.
The adapter tests additionally check namespace substitution and honest fallback wording.

No subagent provider/driver or LLM is mounted by these tests. Native delegation is
a supported host facility, not something supplied by MCP: see the official-package
composition in [README.md](README.md#native-dsh-delegation). A configured native
`subagent` call returns an activation ID first and the final result later via a
completion notice. Without that runner the host must disclose sequential distinct
role passes, never claim independent or concurrent agents. These tests do not
demonstrate child execution, full manuscript generation, or prose quality.

The real Cordis/MCP workflow smoke test plans a 10,000-word project with two
5,000-word chunks, confirms only `outline-check` is ready, and rejects a premature
`chunk-plan` claim. It checks the actual claim's `content` and `result_schema`,
rejects a mismatched `agent_id`, submits the outline-check receipt, and observes
the newly ready planner. Verification remains incomplete and assembly is refused.
These are logical writing tasks: 60,000 / 5,000 would create twelve writing jobs,
not twelve guaranteed concurrent agent processes.

Claims supply both `claim_token` and `result_schema.claim_token`; the host forwards
the full prompt, full schema, and token unchanged and submits the current token
as `result.claim_token`. The workflow test checks same-agent active resume keeps
its token, and missing or stale tokens are rejected. It submits a fixture writer
result, then an actual editor revision request, reclaims the writer, and confirms
the new token differs. Submitting the first attempt's late result is rejected
while the new attempt remains claimed. The host must discard stale child output,
not relabel it with the new attempt token. Repeated fixture prose tests transport
and receipt enforcement only, not writing quality or live child execution.
