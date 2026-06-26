# MCP Sentinel

Use this skill when the user wants to audit MCP server, Cursor, Claude Desktop, Zed, VS Code, or AI agent configuration files for risky command execution, broad filesystem access, inline secrets, or prompt-injection language.

## What This Skill Does

MCP Sentinel is an open-source TypeScript CLI:

https://github.com/fasjdas/mcp-sentinel

It scans common MCP and AI agent config files and reports:

- Interactive shell launchers such as `bash`, `cmd`, PowerShell, or `sh`.
- Package runner startup commands such as `npx`, `pnpm`, `yarn`, `bun`, and `uvx`.
- Broad filesystem access such as root directories, full Windows drives, parent-directory traversal, or unrestricted workspace flags.
- Secret-looking environment keys and inline secret-looking values.
- Destructive startup arguments and pipe-to-shell installers.
- Suspicious prompt-injection or exfiltration language in config text.

## Install Or Run

If the project does not already include MCP Sentinel, clone and build it:

```bash
git clone https://github.com/fasjdas/mcp-sentinel
cd mcp-sentinel
npm install
npm run build
```

Run an audit:

```bash
node dist/cli.js audit /path/to/project
```

Emit JSON:

```bash
node dist/cli.js audit /path/to/project --json
```

Emit GitHub Actions annotations and fail on high severity:

```bash
node dist/cli.js audit /path/to/project --github-annotations --fail-on high
```

## Agent Workflow

1. Identify the project root the user wants scanned.
2. Run MCP Sentinel against that root.
3. Summarize findings by severity first.
4. Explain each finding in practical terms: what access it grants, why it is risky, and what a safer config would look like.
5. Avoid exposing full secret values in chat. Refer to secret keys by name only.
6. If the user asks for a fix, scope MCP server paths to the narrowest useful directory, remove shell wrappers where possible, and replace inline secrets with environment references.

## Supported Config Locations

- `.mcp.json`
- `mcp.json`
- `mcp.config.json`
- `.cursor/mcp.json`
- `.vscode/mcp.json`
- `claude_desktop_config.json`
- `claude_desktop_config.local.json`
- `.zed/settings.json`

## Notes

MCP Sentinel is a static scanner. It provides best-effort risk signals, not a complete security review. Treat findings as prompts for human review and remediation.
