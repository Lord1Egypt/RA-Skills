# post2all setup for OpenClaw

post2all can be used from OpenClaw through the post2all CLI. The hosted MCP server is an alternative when the OpenClaw environment supports remote HTTP MCP with OAuth.

## Recommended: post2all CLI

The ClawHub skill declares `@post2all/cli` as its Node dependency and the `post2all` binary as a runtime requirement.

Verify the CLI:

```bash
post2all --help
```

Create an API key in the user's post2all workspace under **Settings → API Keys**. Prefer providing it through the `POST2ALL_API_KEY` environment variable, or have the user store it locally by running this themselves; it prompts for the key (or reads it from stdin) so the key stays out of shell history and the conversation:

```bash
post2all config set-key
```

Do not run `post2all config set-key <literal key>` on the user's behalf.

Do not place the key in prompts, committed files, screenshots, or logs.

Verify the workspace:

```bash
post2all config whoami --json
post2all accounts --json
```

A successful account listing confirms that OpenClaw can reach the same post2all workspace the user manages in the app.

## Optional environment variable

The CLI also accepts:

```text
POST2ALL_API_KEY
```

This is optional because a user can store the key in the local post2all CLI config instead.

## Alternative: hosted MCP

post2all also exposes a hosted Model Context Protocol server:

```text
https://mcp.post2all.com/mcp
```

The hosted MCP connection uses browser OAuth rather than a post2all API key.

Use this route when the OpenClaw setup supports remote HTTP MCP and the user prefers OAuth-based authorization.

After connecting, verify by asking the connected interface to list post2all accounts.

## First useful test

Start with a draft-only request:

```text
List my connected post2all accounts.
Then turn this idea into platform-specific drafts for the relevant accounts.
Do not publish or schedule anything.
```

This tests authentication, account discovery, capability handling, and post creation without creating a public side effect.

## Useful links

- OpenClaw setup: https://www.post2all.com/openclaw
- post2all: https://www.post2all.com
- MCP docs: https://www.post2all.com/docs/mcp
- API reference: https://www.post2all.com/docs/api-reference
- Agent repository: https://github.com/zexahq/post2all-agent
