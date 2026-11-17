# Install ilearned and set up MCP

## Install or update ilearned

Always prefer the latest published version. Newer releases contain important bug fixes.

If ilearned is not installed yet, or if you want to ensure you have the newest version:

```bash
npm install -g --allow-scripts=@jerrywang121/ilearned @jerrywang121/ilearned
```

Verify the installed version:

```bash
ilearned --version
```

If an older version is already present, the same `npm install -g` command upgrades it. Prefer upgrading before first use or when tools behave unexpectedly.

## Choose storage location (requires permission)

With the user's permission, choose workspace-local storage or user-global storage.

**Workspace-local** (recommended for most projects) — run from the workspace that should own the memory:

```bash
ilearned config init
```

User-global (shared across workspaces):

```bash
ilearned config init --global
```

Notes:

- If the selected config file already exists, `config init` fails rather than overwriting it.
- Never use `--force` without separate, explicit user approval.
- After initialization, run `ilearned config show` from the same working directory and environment that will launch the MCP process.
- If the effective path is unexpected, stop and ask before changing configuration, environment variables, or moving data.

## Set up MCP

Register ilearned as a stdio MCP server.

Inspect any existing `ilearned` entry first; preserve other servers and ask before replacing or changing its database settings.

### OpenClaw

Use OpenClaw’s native MCP registry. Set `--cwd` to the workspace used for `config init`:

```bash
openclaw mcp add ilearned \
  --command ilearned \
  --arg mcp \
  --cwd /absolute/path/to/workspace
```

Verify:

```bash
openclaw mcp doctor ilearned --probe
```

You may need to restart the gateway:

```bash
openclaw gateway restart
```

### Other clients (VS Code, Claude Desktop, etc.)

Other clients use different config-file locations and formats. Example:

```json
{
  "mcpServers": {
    "ilearned": {
      "command": "ilearned",
      "args": ["mcp"]
    }
  }
}
```

Reload the active client and confirm live tool discovery.

## Verification checklist

After setup, confirm the following (ask the user if any step requires elevated permission or changes existing config):

- `ilearned --version` reports a recent version.
- `ilearned config show` points to the expected database / config location.
- The MCP client lists the expected tools (`search`, `add`, `update`, `delete`, `promote`, `demote`, `clear`, `topics_list`, `topics_search`).
- A simple round-trip works (optional but recommended):
  - `add` a temporary test experience under a clear topic such as `test/setup`
  - `search` for it
  - `delete` it (or leave it if the user prefers)

If the active client cannot be checked, state that verification remains incomplete and do not assume the tools are available.

## Important safety notes

- Setup, storage location, encryption, and cross-agent sharing all require explicit user permission.
- The database is plaintext by default. JSONL exports are always plaintext.
- Keep `.ilearned/` gitignored unless the user intentionally chooses to share it.
- Never store secrets or credentials in experiences.
- This skill does not automatically rewrite agent instructions, other skills, or hooks.
