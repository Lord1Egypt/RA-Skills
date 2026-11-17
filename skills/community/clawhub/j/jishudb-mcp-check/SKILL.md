---
name: jishudb-mcp-check
description: >-
  按用户明确要求测试已配置的 JishuDB MCP，适用于只读冒烟测试、工具能力核对、
  全工具验收和验收报告；全工具模式需另行授权临时读写及清理。
  不用于普通知识库查询或首次连接配置。 /
  Run explicitly requested JishuDB MCP smoke checks or all-tools acceptance
  through a configured host connector, with fixtures, cleanup, and a Markdown
  report. Default to read-only smoke checks; not for initial setup or ordinary
  knowledge search.
compatibility: Requires a host agent with a configured JishuDB MCP connector. The all-tools mode requires the jishudb profile. Optional direct-upload coverage requires the host to perform the returned raw HTTP PUT.
metadata:
  author: jishudb
  version: "0.1.4"
  openclaw:
    homepage: https://github.com/x-aijishu/jishudb-skills/tree/main/skills/jishudb-mcp-check
  target-contract: "jishudb-mcp-v2"
  target-contract-digest: "709a2c7dd407c6303ef56b209dacd172e7e8c123bdc5492f578b610eb791544a"
---

# JishuDB MCP Check

Run an explicitly requested functional acceptance check through the host's
configured JishuDB MCP connector. Deliver a Markdown report with observed
results and cleanup status.

## At a glance

| Item | Details |
| --- | --- |
| Use when | A configured connector needs an explicit smoke test or all-tools acceptance run. |
| Delivers | Observed test results, coverage gaps, cleanup status, and a Markdown acceptance report. |
| Requires | A configured host MCP connector; the jishudb profile and scoped approval for all-tools mode. |
| Does not | Perform initial setup, use private HTTP APIs, or mutate existing user resources. |

## Use this skill when

- The user explicitly asks to smoke-test a configured JishuDB MCP connector.
- The user requests a tool-catalog or capability check against the bundled contract.
- The user requests an isolated all-tools acceptance run with temporary fixtures.
- The user needs a functional acceptance report with observed results and cleanup.

## Do not use this skill when

Do not use this skill merely because a connection fails or a document query
returns no results. Use `jishudb` for initial setup and connection repair, or
`jishudb-search` for ordinary retrieval. An all-tools request still requires
the mutation approval described below.

## Agent workflow

If the host does not expose the selected JishuDB connector, mark the connection
precondition `BLOCKED`, report overall `PARTIAL`, and leave dependent tests
unrun. State whether host reconnection, authorization, or separate setup is
needed. If a capability call can be made but fails, apply the preflight `FAIL`
rule and preserve its observed cause. Do not invent results, replace MCP checks
with local artifacts, or install another database to make the test pass.
Setup/repair is a separate user-authorized operation; after it completes, rerun
the checks through the intended host connector.

This is a consumer-level functional test. Do not claim raw MCP envelope,
header, or protocol conformance unless the host exposes those surfaces.

### Modes

- `smoke`: read-only connection and capability checks. Use this by default
  when the user does not specify a mode.
- `all-tools`: isolated read/write acceptance run across the complete visible
  `jishudb-mcp-v2` catalog.

Read [references/test-cases.md](references/test-cases.md) and
[references/report-template.md](references/report-template.md) before either
mode. Also read
[references/contract-baseline.md](references/contract-baseline.md) to compare
the running catalog with this Skill version. For `all-tools`, also read
[references/fixture-values.md](references/fixture-values.md).

### Safety rules

1. Never print, summarize, save, or place in the report:
   - the MCP bearer;
   - Base64 fixture values;
   - direct-upload Authorization values;
   - connector credentials;
   - local paths;
   - complete imported URLs containing queries or fragments.
2. In `all-tools`, mutate only IDs recorded during the current run.
3. Never delete or update an existing user resource.
4. Existing sources may be read or synchronized only with explicit user
   approval naming the source or knowledge base.
5. Do not create intentionally huge, malformed, or malicious files to force
   failed or cancellable jobs.
6. Do not use private JishuDB HTTP APIs. The only allowed non-MCP request is
   the one-time raw-byte `PUT` returned by `kb_prepare_upload`.
7. If cleanup fails, the overall result is `FAIL` and the report must list the
   remaining run-scoped IDs.
8. `https://example.com/` is the packaged, pre-approved public fixture for
   `kb_import_url`. Do not substitute another external URL without user
   approval.

### Result states

- `PASS`: the required behavior and assertions were observed.
- `FAIL`: prerequisites existed but behavior or output was wrong.
- `SKIP`: an optional server capability or optional host observation is
  unavailable.
- `BLOCKED`: the connector is absent, or a visible tool's positive path
  requires an external prerequisite or host capability that was not supplied.

Use `PARTIAL` overall when there are no failures but at least one case is
`BLOCKED`.

### Preflight

1. Confirm the host exposes the JishuDB connector. If absent, report the
   blocked precondition and stop before calling tools or creating fixtures.
2. Call `kb_get_capabilities`.
3. Stop with `FAIL` if the call fails or the tool contract is not
   `jishudb-mcp-v2`.
4. Record the reported transport, protocol version, server version, revision,
   profile, tools, and upload modes.
5. Confirm `kb_create_memo` is absent.
6. Compare the reported tool names with the packaged contract baseline:
   - any missing baseline tool is `FAIL`;
   - any additional tool means this Skill is older than the server, so retain
     the known tests, list the new tool as untested, and make the overall
     result at most `PARTIAL`;
   - if a runtime contract digest is exposed and differs from the packaged
     digest, report contract drift and make the result at most `PARTIAL`.
7. If the host exposes its loaded tool catalog, compare its names with the
   capability tool list. If it does not, record this observation as `SKIP`.

For `smoke`, execute only the smoke cases and return the report.

For `all-tools`, require profile `jishudb`. Before mutating anything, tell the
user that the run will create one temporary knowledge base, three fixture
documents, one Note, and related ingest jobs, then delete its own resources.
Obtain one approval for that complete scope.

### Run state

Generate and retain:

```text
runId: filesystem-safe UTC timestamp plus a short random suffix,
       for example 20260820T160500Z-a7f2
kbId: jishudb-mcp-check-<runId>
noteId: newly generated UUID
noteCreatedAt: one RFC 3339 timestamp reused for note_create replay
```

Use `runId` in the temporary KB name, description, uploaded filenames, Note
title/content, and idempotency keys.

Record every returned `documentId`, `jobId`, Note `updatedAt`, optional
`uploadId`, and any approved source ID. Never reconstruct IDs from names.

Maintain one case record with:

```text
caseId, tool, expected, evidence, result, errorCode, cleanupImpact
```

When the host hides `_meta["io.jishudb/errorCode"]`, use
`errorCode=not-exposed` and retain only a sanitized client-visible error.

### Execution

Follow the order in [references/test-cases.md](references/test-cases.md).

- Use the exact precomputed fixture values; do not recalculate or alter bytes.
- Poll asynchronous jobs every 2 seconds for at most 120 seconds.
- For Note automatic refresh, allow the 30-second debounce plus processing,
  but stop after 120 seconds and report the last observed state.
- For expected rejection tests, verify the protected resource did not change.
- Continue independent read-only diagnostics after a case failure when safe,
  but stop mutating the failed resource.
- If direct upload is enabled but the host cannot perform the returned `PUT`,
  mark its positive path `BLOCKED` and use the PDF Base64 fixture for downstream
  document tests.

### Cleanup

Attempt cleanup even after failures:

1. Delete the run Note if it still exists, using its latest recorded
   `updatedAt`.
2. Delete the designated TXT document if it still exists.
3. Delete the run KB using the exact recorded `kbId`.
4. Verify reads return `NOT_FOUND` or the host-visible equivalent.

Never broaden cleanup to similarly named resources.

### Report

Render the final answer using
[references/report-template.md](references/report-template.md).

Include:

- this Skill version and packaged contract baseline;
- counts for `PASS`, `FAIL`, `SKIP`, and `BLOCKED`;
- all advertised tools without a positive-path test;
- the first actionable failure;
- cleanup status and remaining run IDs;
- whether stable error metadata was exposed by the host;
- a redaction statement.

Do not claim success merely because a tool call returned. Apply every listed
assertion to the returned evidence.

## Resources

- [`assets/canary.txt`](assets/canary.txt): Use only in the all-tools fixture cases described by the test cases and fixture-values references; preserve exact bytes.
- [`assets/canary.pdf`](assets/canary.pdf): Use only in the all-tools fixture cases described by the test cases and fixture-values references; preserve exact bytes.
- [`assets/canary.md`](assets/canary.md): Use only in the all-tools fixture cases described by the test cases and fixture-values references; preserve exact bytes.

## Discovery

### Keywords

- Chinese: MCP冒烟测试、工具验收、能力核对、验收报告、临时资源清理.
- English: JishuDB MCP smoke test, all-tools acceptance, tool catalog, contract baseline, fixture cleanup.

### Example requests

- “对已配置的JishuDB MCP做一次只读冒烟测试。”
- “核对可用工具与打包契约，输出验收报告。”
- “Run all-tools acceptance in an isolated scope and report fixture cleanup.”
- “Smoke-test my configured JishuDB connector and list untested capabilities.”

### Nearby but different

- Initial setup or a connection repair → `jishudb`.
- Ordinary knowledge-base questions → `jishudb-search`.
