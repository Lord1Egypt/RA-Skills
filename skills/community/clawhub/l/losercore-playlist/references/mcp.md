# MCP connection and tool inputs

The remote transport is Streamable HTTP: https://losercoreplaylist.com/mcp . It is public and stateless; no environment variables or API keys are required. Use an MCP host that supports remote Streamable HTTP. The browser application remains separate from this MCP connection.

Claude Code example:

```sh
claude mcp add --transport http losercore-playlist https://losercoreplaylist.com/mcp
```

If remote MCP is unavailable in the host, use Node.js 22.12+ and the bundled script from the skill directory:

```sh
node scripts/mcp-call.mjs tools/list
node scripts/mcp-call.mjs tools/call '{"name":"search_playlist","arguments":{"query":"quiet","limit":4}}'
node scripts/mcp-call.mjs tools/call '{"name":"get_creation_template","arguments":{"template":"beanie-loser"}}'
node scripts/mcp-call.mjs tools/call '{"name":"prepare_video_project","arguments":{"tracks":[{"title":"My original song","artist":"Me"}],"language":"en"}}'
```

The final example uses the three default original captions. For custom captions pass exactly three nonempty strings of at most 200 characters. Use your own song metadata; the server does not verify music rights. `language` accepts en, zh or id. Other exposed protocol reads: resources/list, resources/read, prompts/list, prompts/get. List first to learn current resource URIs and prompt arguments.

Read the JSON-RPC `result.structuredContent` for tool data. A tool result with `isError: true`, or a protocol `error`, is a failure, not a completed generation. For project preparation, save only `result.structuredContent.project`, excluding the response wrapper; the returned filename/workspaceUrl/nextSteps explain the browser handoff. The script prints JSON to stdout and diagnostics to stderr, writes no files and cannot render media.

Requests and replies are bounded; the remote endpoint caps request bodies at 16 KiB. Inputs pass through the selected agent host and Losercore server. No cloud model credentials or payment actions are exposed. Public documentation: https://losercoreplaylist.com/developers/mcp .
