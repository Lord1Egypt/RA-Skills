## Built-in MCPs

OmO includes 3 built-in MCP (Model Context Protocol) servers that provide external tool access.

### websearch (Exa)

Provides web search capabilities via the Exa search API.

Tool: `websearch_web_search_exa`

Parameters:
- query (required): Search query string
- numResults: Number of results (default: 8)
- category: Filter by "company", "research paper", or "people"
- contextMaxCharacters: Max chars for context (default: 10000)
- livecrawl: "fallback" or "preferred"
- type: "auto" (balanced) or "fast" (quick)

Example usage by agent:
```
websearch_web_search_exa(query="React Server Components best practices", numResults=5)
```

### context7 (Documentation)

Provides up-to-date documentation and code examples for any programming library.

Tools:
- `context7_resolve-library-id`: Resolve package name to Context7 library ID
- `context7_query-docs`: Query documentation for a specific library

Workflow:
1. Resolve: `context7_resolve-library-id(libraryName="next.js", query="how to set up app router")`
2. Query: `context7_query-docs(libraryId="/vercel/next.js", query="app router setup")`

Limit: Max 3 calls per question.

### grep_app (GitHub Code Search)

Search for real-world code patterns across 1M+ public GitHub repositories.

Tool: `grep_app_searchGitHub`

Parameters:
- query (required): Literal code pattern to search for
- language: Filter by language (e.g., ["TypeScript", "TSX"])
- repo: Filter by repository (e.g., "facebook/react")
- path: Filter by file path
- useRegexp: Enable regex matching
- matchCase: Case sensitive search

Important: Searches for literal code patterns (like grep), not keywords.
- Good: `useState(`, `import React from`, `async function`
- Bad: "react tutorial", "best practices"

### Custom MCPs

Additional MCPs can be added via skill frontmatter or oh-my-opencode.json:

```json
{
  "mcps": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@my-org/mcp-server"],
      "env": {
        "API_KEY": "..."
      }
    }
  }
}
```
