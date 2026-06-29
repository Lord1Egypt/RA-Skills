# ModelBound MCP — Recipes

All examples assume `MODELBOUND_API_KEY` is set. Endpoint: `https://mcp.modelbound.co`.

## 1. Pull a team skill into `./.claude/`

```jsonc
// 1. scope to the team
{ "jsonrpc":"2.0","id":1,"method":"tools/call",
  "params":{"name":"gateway.setWorkspace","arguments":{"team":"acme"}}}

// 2. find it
{ "jsonrpc":"2.0","id":2,"method":"tools/call",
  "params":{"name":"search.all","arguments":{"q":"postgres migrations","types":["skill"]}}}

// 3. fetch the body (id from step 2)
{ "jsonrpc":"2.0","id":3,"method":"tools/call",
  "params":{"name":"files.get","arguments":{"id":"skill_01H..."}}}
```

Write the returned `content` to `./.claude/skills/postgres-migrations/SKILL.md`.

## 2. Answer a question from team knowledge

```jsonc
{ "jsonrpc":"2.0","id":1,"method":"tools/call",
  "params":{"name":"search.summary","arguments":{
    "q":"how do we rotate Stripe webhook secrets?",
    "max_chunks": 6
  }}}
```

Response includes `answer` plus an array of `citations` with `file_id` and `url`. Follow up with `files.get` if the user asks for the full source.

## 3. Propose a fix back to a team skill

```jsonc
// 1. fetch current content
{ "jsonrpc":"2.0","id":1,"method":"tools/call",
  "params":{"name":"files.get","arguments":{"id":"skill_01H..."}}}

// 2. propose the edit (NEVER use skills.update)
{ "jsonrpc":"2.0","id":2,"method":"tools/call",
  "params":{"name":"skills.proposeDraft","arguments":{
    "skill_id":"skill_01H...",
    "content":"<new SKILL.md body>",
    "summary":"Fix typo in step 3 + add note about RDS Proxy"
  }}}
```

Response: `{ "review_url": "https://modelbound.co/skills/.../review/..." }`. Show that URL to the user — a teammate approves it in the ModelBound UI.
