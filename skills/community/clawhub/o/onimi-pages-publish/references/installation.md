# Install Onimi Pages

Choose one installation source. The default suite path explicitly prepares Creator and Publish, then
connects the current agent only when a cloud task needs it.
Installation does not authorize access or establish production service readiness.
One installation task checks and adds both modules. Creation and prepublish checks use the current
agent's model; no separate local model installation is needed.

## npm

The npm package bundles the complete skill and a dependency-free local installer.
It does not fetch skill files from GitHub. Requires Node.js 20 or later and npm.

```sh
npx --registry=https://registry.npmjs.org onimi-pages-publish@latest install --suite --agent codex
```

Replace `codex` with `claude-code` or `cursor`. For another client, inspect its documented
personal skills directory and use `install --dir /absolute/path/to/skills` instead.
The suite installer creates missing `onimi-pages-creator` and `onimi-pages-publish` folders inside that
parent directory. It preserves every existing folder and local change. If an older Publish module was
already present, adding Creator does not upgrade Publish: check both versions before claiming the
current suite is ready. Update the old module through its original channel while preserving personal
changes, and explain when a safe update is unavailable. Omit `--suite` only for the
advanced legacy task of publishing finished HTML without Creator. Run
`npx --registry=https://registry.npmjs.org onimi-pages-publish@latest --help` for options.
Only install for the current agent. Restart or reload that agent if needed.

Check the verified channel states in
https://downloads.onimi.ai/skills/manifest.json before using a registry source. Run the
`@latest` suite command only when `skills.publish.channels.npm.available` is true and its channel
version equals `skills.publish.version`; an older available Publish package may not contain the suite
installer. Otherwise use a current channel from that manifest.

## Direct download

For the suite, read the complete `skills.creator.archive.url`, `skills.creator.archive.sha256`, and
`skills.creator.archive.size` fields plus the matching `skills.publish.archive.url`,
`skills.publish.archive.sha256`, and `skills.publish.archive.size` fields from the stable manifest:

- https://downloads.onimi.ai/skills/manifest.json

Download both exact immutable, versioned archives. Verify each byte size and SHA-256 with
`shasum -a 256` (macOS), `sha256sum` (Linux), or PowerShell
`Get-FileHash -Algorithm SHA256` before extracting.
Each ZIP contains one complete Skill directory. Add only a missing `onimi-pages-creator/` or
`onimi-pages-publish/` directory to the current agent's personal skills directory. Do not overwrite
either existing directory or local changes. The advanced Publish-only path needs only the Publish entry.

| Client | Personal skills parent directory |
| --- | --- |
| Codex | `~/.agents/skills` |
| Claude Code | `~/.claude/skills` |
| Cursor | `~/.cursor/skills` |

## ClawHub

Listing: https://clawhub.ai/mariohazy/onimi-pages-publish
Publisher: `mariohazy`; skill: `@mariohazy/onimi-pages-publish`.
The pinned ClawHub CLI requires Node.js 22 or later; use another verified channel on Node.js 20.

```sh
npx --registry=https://registry.npmjs.org clawhub@0.23.3 install @mariohazy/onimi-pages-publish
```

ClawHub installs into its configured workspace skill directory by default. Use its
`--workdir` and `--dir` options to select only the current agent's documented skill
parent directory, or move the complete downloaded folder there. Run `clawhub --help`
to check these options. Do not bypass registry security review if a release is pending.

## GitHub

Official repository: https://github.com/zlch-oceanai/onimi-pages-publish

```sh
npx --registry=https://registry.npmjs.org skills@1.5.26 add zlch-oceanai/onimi-pages-publish --skill onimi-pages-publish --global
```

Select only the current agent. If it cannot run commands, use its documented skill
import UI or copy the complete `skills/onimi-pages-publish` folder from the repository.
Other clients require their own custom-skill and remote MCP support; a brand name
alone does not establish compatibility in every desktop, web or mobile version.

The bundled manager applies only when a direct-download installation has
`.onimi-skill.json` beside `SKILL.md`. If the receipt is absent, use that channel's native
update flow. For a receipt-backed installation, resolve the installed Skill directory from its
`SKILL.md` path and invoke the manager by absolute path without changing the user's
workspace directory. Run
`node /absolute/path/to/onimi-pages-publish/scripts/manage.mjs status` locally,
`node /absolute/path/to/onimi-pages-publish/scripts/manage.mjs check` for the daily
non-blocking update check, and only after approving the displayed version run
`node /absolute/path/to/onimi-pages-publish/scripts/manage.mjs update --confirm onimi-pages-publish@<version>`.
The manager protects all edits and additional files, verifies the immutable archive,
keeps a backup, and atomically rolls back a failed switch. npm, ClawHub, GitHub, and
agent-host update commands remain specific to those channels.

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
