# Install Onimi Pages & Slides

Install the unique `onimi-pages` Skill from the reviewed source repository
https://github.com/zlch-oceanai/onimi-pages using the current Agent's supported
Skill installer. A supported plugin host can import the root portable plugin
and MCP configuration together. Repository hosting does not imply marketplace approval.

This source package does not require the direct stable manifest or an npm release.
It contains no direct-download installer or update manager. Preserve existing folders
and personal changes; follow [migration.md](migration.md) before adding this Skill
beside old Creator/Publish installations. Host-managed copies use the host's lifecycle.
Codex uses `~/.agents/skills`, Claude Code `~/.claude/skills`, Cursor `~/.cursor/skills`;
verify the current Agent's actual directory before installing.
Installation does not connect an account, save a draft or publish.

## Configure the connection

Remote MCP: `https://onimi.ai/mcp` (Streamable HTTP, browser OAuth with PKCE).

The exact tool set depends on the deployed service version. Before changing a published
project's visibility, the agent checks the tools it actually discovered. If
`onimi_set_visibility` is absent, the release remains valid but its visibility remains
unchanged; use the project's settings in https://onimi.ai/dashboard. The agent must not
report a private or unlisted release as publicly listed.
No static Authorization header or developer token is needed. Skill installation
alone does not necessarily register the MCP server. `agents/openai.yaml` declares
a dependency for hosts that support it; other hosts need their native MCP setup.

### Codex

Check `codex --version` and `codex mcp add --help` before using these options:

```sh
codex mcp add onimi-pages --url https://onimi.ai/mcp --oauth-client-registration dcr --oauth-resource https://onimi.ai/mcp
codex mcp login onimi-pages --oauth-client-registration dcr --scopes project:read,project:write,draft:read,draft:write,template:read,release:read,release:publish,collaboration:manage
```

The add operation may start authorization itself. Skip login if already connected.
If the installed version does not expose these flags, use its documented remote
MCP configuration or update the client; do not invent unsupported options.

### Claude Code

```sh
claude mcp add --transport http --scope user onimi-pages https://onimi.ai/mcp
```

Inside Claude Code run `/mcp`, select Onimi Pages and Authenticate.

### Cursor

Merge this server into the personal `~/.cursor/mcp.json` configuration using the
client's MCP settings. Preserve other servers and existing settings:

```json
{ "mcpServers": { "onimi-pages": { "url": "https://onimi.ai/mcp" } } }
```

Use the connection/authorization action shown by Cursor. Reload if needed.

### Kimi Code

Use the installed client's `/mcp-config` setup to add the HTTP service, then
`/mcp-config login onimi-pages` to start browser authorization. Check the client's
help for version-specific setup syntax.

### Other clients

Use the client's documented custom remote MCP connection screen. Add the URL
above and start its OAuth flow. Do not substitute an API key when OAuth is missing.

## Browser approval and verification

The user signs in to Onimi Pages if needed, reviews requested scopes, and approves
the connection. The agent must not click consent for the user or request tokens in
chat. The client owns credential storage and refresh.

Before authorization, call `onimi_get_connection`. Reuse it only for the same account when its effective
scopes cover the task. After approval, call it again; it reports connection identity and scopes but
deliberately leaves module installation to a client-local check. If an older deployed service does not
expose this tool, use `onimi_list_projects` as the read-only compatibility check; an empty list is valid.
Do not create a project, read a private draft, acquire a template, or publish as an installation test.
Revoke access in `https://onimi.ai/dashboard/connections` when no longer needed. This does not take
already published pages offline.

If discovery returns 404, a protection page or a login HTML document, installation
cannot repair the hosted service. Explain the unavailable connection; do not report
success or switch endpoints to a test environment. Dashboard upload is the fallback.
