---
name: context7
description: >-
  Look up current, accurate documentation and code examples for any library or
  framework using context7-mcp. Use when an agent needs to know how to use a
  library (APIs, configuration, examples), wants to avoid hallucinating outdated
  API details, or needs to verify a method signature, config schema, or
  integration pattern. Triggers on phrases like "how do I use X", "what's the
  API for Y", "show me an example of Z", "check the docs for", "latest syntax
  for", "how to configure", or any task where current library documentation
  would improve accuracy. Requires npx and network access; no API key needed.
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: "📚"
    homepage: https://context7.com
---

# context7

Look up live, accurate documentation for any library via the context7-mcp server. Prevents hallucinated APIs by fetching real, indexed documentation at query time.

## When to Use

Use this skill any time you need accurate, current details about a library — method signatures, config schemas, integration examples, version-specific behaviour. context7 indexes 5000+ libraries including OpenClaw, LangChain, Next.js, Supabase, FastAPI, and more.

**Do not rely on training data alone** for library-specific questions; use this skill instead.

## How context7-mcp Works

context7-mcp is a Model Context Protocol (MCP) server that queries [context7.com](https://context7.com) for indexed documentation. It exposes two tools:

- `resolve-library-id` — resolve a library name to its context7 library ID
- `query-docs` — fetch documentation snippets for a specific library + query

The server runs via `npx -y @upstash/context7-mcp` with no auth required.

## Workflow

### Step 1: Resolve the library ID

Call `resolve-library-id` with the library name and your task as the query. Pick the result with the highest **Benchmark Score** and **Source Reputation: High or Medium** that matches your intent.

```
resolve-library-id(
  libraryName: "openclawai",
  query: "how to configure mcp.servers"
)
```

Use the returned library ID (format: `/org/project`) in step 2.

### Step 2: Fetch documentation

Call `query-docs` with the library ID and a specific, task-focused query. Narrow queries return better results than broad ones.

```
query-docs(
  libraryId: "/websites/openclaw_ai",
  query: "mcp.servers configuration add local stdio process"
)
```

### Step 3: Apply the result

Use the returned code snippets and prose directly. They come with source URLs — cite them when precision matters.

## Tips

- **Narrow queries beat broad ones.** "How to authenticate with JWT in Express" beats "authentication".
- **Try multiple queries** if the first result is shallow — rephrase around what you actually need to do.
- **Use the source URL** in results to fetch more context with `web_fetch` if a snippet is incomplete.
- **Call `resolve-library-id` once per library per session** — cache the ID rather than resolving it repeatedly.
- **Don't call either tool more than 3 times per question** — if 3 calls haven't found it, use the best result you have.

## OpenClaw MCP Integration

If context7-mcp is configured as an OpenClaw MCP server, the tools (`resolve-library-id`, `query-docs`) appear natively in your tool surface without running a subprocess. Apply the same workflow — the tool names and arguments are identical.

To check if it's configured: run `/mcp show` and look for `context7`.

To configure it (operator slash command):
```
/mcp set context7="{\"command\":\"npx\",\"args\":[\"-y\",\"@upstash/context7-mcp\"]}"
```

## Manual Testing

To verify context7-mcp works on your system:
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | npx -y @upstash/context7-mcp 2>/dev/null | grep '"name"'
```

Expected output includes `resolve-library-id` and `query-docs`.
