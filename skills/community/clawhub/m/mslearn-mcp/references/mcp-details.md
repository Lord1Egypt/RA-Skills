# Learn MCP setup and recovery

Baseline checked 2026-10-30: Learn CLI 1.0.0 discovery, search, fetch and code search. Confirm the installed OpenClaw version before changing configuration; its [registry documentation](https://docs.openclaw.ai/cli/mcp/registry) governs Gateway ownership.

## OpenClaw native MCP

`openclaw mcp list`, `show`, `status` and `doctor` without `--probe` inspect saved configuration while the Gateway runs. A saved definition does not prove tool reachability or visibility to the intended agent.

Current CLI mutations and live probes require a stopped local Gateway. Prefer supported Control UI setup or the standalone Learn CLI while it runs. During authorized maintenance:

```bash
openclaw mcp add mslearn --url https://learn.microsoft.com/api/mcp --transport streamable-http
openclaw mcp doctor mslearn --probe
openclaw mcp status --verbose
```

Use explicit Streamable HTTP; older builds can default to SSE. Verify tools in the intended agent after the applicable reload/restart. `openclaw mcp reload` affects only its CLI process, not another Gateway. Agent/runtime filters still apply.

Within an authorized configuration change, `openclaw mcp tools mslearn --include 'microsoft_docs_search,microsoft_docs_fetch'` restricts saved tools; `openclaw mcp unset mslearn` removes the definition. Do not reset unrelated configuration.

## Standalone clients

The [main workflow](../SKILL.md) gives pinned Microsoft CLI commands; `doctor --format json` checks runtime, endpoint, handshake and tools. `mslearn setup` installs Microsoft's own discovery skill and is unnecessary here. Review release notes before changing the pin.

For an **existing mcporter host**, call without saving configuration:

```bash
mcporter call https://learn.microsoft.com/api/mcp.microsoft_docs_search query="Azure Functions triggers"
```

For requested persistent setup (syntax baseline 0.16.0):

```bash
mcporter config add mslearn https://learn.microsoft.com/api/mcp --scope home
mcporter list mslearn --schema
mcporter call mslearn.microsoft_code_sample_search query="Python blob upload" language=python --output json
```

Removal: `mcporter config remove mslearn`. Its `./config/mcporter.json` and `~/.mcporter/mcporter.json` use `mcpServers`; OpenClaw's registry is separate. The older `config add --name ... --url ... --type http` form is invalid.

## Recovery

| Symptom | Check |
| --- | --- |
| Saved server, missing tools | Agent filters, runtime availability and reload requirements |
| Probe refuses during operation | Use Control UI/standalone CLI; no unrequested Gateway stop |
| Connection failure | CLI `doctor`, host DNS/proxy |
| Unknown tool/parameter | Live schema discovery |
| HTTP 429/repeated timeouts | Stop; report unavailable evidence |
| HTTP 405 from endpoint in browser | Use an MCP client; browser GET is not discovery |
| Off-topic results | Add product, feature and version/SKU |

Experimental [Microsoft profiles](https://github.com/MicrosoftDocs/mcp) can change: `?maxTokenBudget=2000` approximately limits search tokens; `/openai-compatible` targets Deep Research clients and is unnecessary for this workflow.

Sources: [Microsoft MCP](https://github.com/MicrosoftDocs/mcp), [release notes](https://learn.microsoft.com/en-us/training/support/mcp-release-notes), [CLI](https://www.npmjs.com/package/@microsoft/learn-cli), [OpenClaw registry](https://docs.openclaw.ai/cli/mcp/registry).
