# Options, sources and limits

## Parameters

Run `node "{baseDir}/scripts/brief.mjs" help` for the concise command list.

| Option | Meaning | Default |
|---|---|---|
| `--workspace PATH` | Existing, writable agent workspace; required | None |
| `--days 1..30` | Inclusive calendar days ending today | 1 |
| `--limit 1..20` | Maximum selected items | 8 |
| `--timezone IANA` | Such as `Asia/Shanghai`, `Europe/London`, `America/New_York` | UTC |
| `--language zh-CN\|en` | Saved heading and model brief language | zh-CN |
| `--topics "AI,开源"` | Up to 8 comma-separated terms; OR matches against title and short excerpt | No topic filter |
| `--feeds FILE` | UTF-8 JSON array of 1–8 named public HTTPS feeds | Three sources below |

Latin terms match word boundaries, so `AI` does not match `daily`. Chinese terms match substrings. Matching is keyword based, not semantic search. Filtering may miss synonyms. Items sort newest first and deduplicate normalized URLs and headlines. Tracking parameters are removed; separate stories about the same event may still appear.

The current model then checks semantic relevance and user exclusions before writing. Only cited source IDs appear in the saved report. If every candidate is unsuitable, a draft containing exactly `NO_MATCHING_ITEMS` produces a deterministic empty result. The original evidence remains unchanged for review.

Only dated RSS 2.0 and Atom entries with public HTTPS article links are supported. RSS 1.0/RDF, HTML pages, feeds requiring authentication and legacy non-UTF-8 encodings are not supported. Source dates are those supplied by the publisher; an Atom `updated` timestamp may represent an edit rather than original publication.

## Default official sources

These are publisher-operated feeds. Direct HTTPS fetch and parsing were checked on **2026-10-22**, not a promise of future uptime or freshness.

- OpenAI News: `https://openai.com/news/rss.xml`
- Google AI: `https://blog.google/technology/ai/rss/`
- GitHub Changelog: `https://github.blog/changelog/feed/`

To change topics, use relevant sources as well as keywords. For example, the defaults will not provide comprehensive sports or local news. When requested, write a separate feed configuration in the workspace using the file-write tool:

```json
[
  {"name":"OpenAI News","url":"https://openai.com/news/rss.xml"},
  {"name":"Google AI","url":"https://blog.google/technology/ai/rss/"}
]
```

Then add `--feeds "ABSOLUTE_PATH_TO_JSON"`. Existing files are not edited automatically. Feed selection is not saved as a global preference; repeat the option on the next run. No cookies, passwords or API keys are sent.

## Local output and privacy

`collect` writes one evidence JSON file in `.mochi-daily-brief/`; the agent writes the matching draft there. `save` writes the Markdown report in `daily-briefs/`. Both directories are inside the specified workspace. Evidence contains titles, short excerpts, source URLs, dates and collection errors. Output is local; this script sends no user data to MochiLab. Your OpenClaw model still processes the evidence under that model service's own privacy and billing terms. Public feed servers see the request IP and user agent.

Unique filenames preserve earlier reports. No cleanup/deletion runs automatically. The user can review and remove their own old evidence/reports manually. Symlink/junction workspaces or output directories are refused; choose a real allowed workspace directory instead of bypassing the check.

## Network and failure behavior

Each feed has an 18-second deadline including up to 3 redirects. At most 3 feeds are fetched concurrently. Requests validate TLS certificates, require public HTTPS domains on port 443, reject private/reserved DNS answers and pin a validated address for the connection. Both redirect targets and their DNS are checked again. No localhost/internal feed exception is provided.

Limits: 1 MiB downloaded compressed bytes, 2 MiB expanded XML, 500 entries per source, 20,000 XML nodes and 32 levels of nesting. DTDs and declared entities are rejected. These limits can cause a large or malformed feed to fail rather than be partially trusted. The parser never evaluates scripts or expands external entities. A UTF-8 RSS/Atom document is required; HTML error pages are not news.

The collector does not automatically use an HTTP proxy. A host requiring a proxy, blocking direct HTTPS, lacking trusted certificates or resolving to private addresses may fail. Fix the actual host/network issue through normal administration; do not disable TLS verification or remove address checks. Partial failures are recorded. If all sources fail, the report has no eligible items and lists the errors; this is not evidence of no news elsewhere.

## Installation format and self-check

Extract the ZIP once. The final shape must be `WORKSPACE/skills/mochi-daily-brief/SKILL.md` with its `scripts` and `references` beside it, not a doubly nested folder. Install in the agent workspace you actually use. The shared alternative is `~/.openclaw/skills/mochi-daily-brief/` when deliberately making the Skill available across agents. Check `openclaw skills check`, then start a new chat if an existing session has not refreshed. If the Skill is present but unavailable, inspect tool permissions and the Node requirement.

Official format/path references checked 2026-10-22:

- https://docs.openclaw.ai/tools/skills
- https://docs.openclaw.ai/clawhub/skill-format

For maintainers, offline fixtures run with Node 24+:

```text
node --test --test-isolation=none "{baseDir}/tests/brief.test.mjs"
```

The fixture suite does not contact live sites, schedule tasks or alter OpenClaw configuration. Passing it verifies the supplied script cases, not installation on every OpenClaw host or a model's factual accuracy.
