# Setup and recovery

Baseline checked 2026-11-15 from a Linux host: handshake, tool discovery and one stateless search against every endpoint in the [main workflow](../SKILL.md), plus agent runs on OpenClaw 2026.11.2. The stateless call there needs only `curl`; nothing below is required for lookups.

## Vendor notes

| Vendor | Server | Auth | Notes |
| --- | --- | --- | --- |
| Microsoft | Microsoft Learn MCP Server | none | No `locale` or `product` arguments; search returns Q&A and blog items too, prefer product docs; `microsoft_docs_fetch` reads only `learn.microsoft.com` pages |
| AWS | AWSKnowledgeMCP | none | `topics` narrows search (`reference_documentation`, `troubleshooting`, `cdk_docs`, `cloudformation` and others); `aws___read_documentation` pages with `start_index` |
| Google | Developer Knowledge API | API key | Public preview, English only; covers Google Cloud, Firebase, Android, Chrome, Flutter, Gemini API and more; `get_documents` takes `names` exactly as search returns them; `answer_query` has a small daily quota, prefer search |
| Cloudflare | docs-ai-search | none | One search tool; results include the page text and run to about 70 KB, so the cap keeps the top results |
| OpenAI | openai-docs-mcp | none | Search hits often carry no text and stay large even with `limit`: read the page with `fetch_openai_doc`; `get_openapi_spec` returns one endpoint's schema |
| Anthropic | claude-platform-docs | none | Claude API, SDKs and Managed Agents; `get_doc` accepts a search result URL or a path starting with `/docs/en/`; `sdk_languages` (for example `["python"]`) trims code samples and shortens long pages |

Google key: in a Google Cloud project, enable the Developer Knowledge API, create an API key restricted to that API and export it as `GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY`. Send it only in the `X-Goog-Api-Key` header, never in the URL. Default quotas are per project: 100 searches and 100 document reads per minute.

## OpenClaw native MCP (optional)

Registration is optional: it gives agents typed tools in place of a shell call, and the skill uses connected tools first when they exist. Confirm the installed OpenClaw version first; its [registry documentation](https://docs.openclaw.ai/cli/mcp/registry) governs Gateway ownership. Current CLI mutations and live probes require a stopped local Gateway; do not stop a Gateway merely for a lookup.

```bash
openclaw mcp add aws-docs --url https://knowledge-mcp.global.api.aws --transport streamable-http \
  --include 'aws___search_documentation,aws___read_documentation,aws___get_regional_availability'
openclaw mcp set google-docs '{"url":"https://developerknowledge.googleapis.com/mcp","transport":"streamable-http","headers":{"X-Goog-Api-Key":"${GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY}"},"toolFilter":{"include":["search_documents","get_documents"]}}'
openclaw mcp doctor aws-docs --probe
```

Use explicit Streamable HTTP; without it OpenClaw assumes SSE. Keep an include filter so only search and read tools are exposed. Remove with `openclaw mcp unset <name>`. Do not reset unrelated configuration.

## Recovery

| Symptom | Check |
| --- | --- |
| Unknown tool or argument | `tools/list` on the same endpoint, then use the live schema |
| Google answers "Permission denied on the service" | Key missing, API not enabled on the key's project, or key restricted to other APIs |
| HTTP 405 or HTML from an endpoint | It was opened with GET; send the POST from the main workflow |
| Empty or cut result | Extract the passage with the `grep -o` filter from the main workflow, or lower `limit`; for OpenAI read the page |
| HTTP 429 or repeated timeouts | Stop; report unavailable evidence |
| Off-topic results | Add product, feature and version or tier to the query |
| Saved server, missing tools | Agent tool filters, runtime availability and reload requirements |

Sources: [Microsoft Learn MCP](https://github.com/MicrosoftDocs/mcp), [AWS Knowledge MCP](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server), [Google Developer Knowledge MCP](https://developers.google.com/knowledge/mcp), [Cloudflare MCP servers](https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare), [OpenAI Docs MCP](https://developers.openai.com/api/docs/docs-mcp), [Claude Platform docs MCP](https://platform.claude.com/docs/mcp), [OpenClaw registry](https://docs.openclaw.ai/cli/mcp/registry).
