# @proofai/mcp-server

MCP Server for ProofAI — plug AI compliance into Claude Code.

## Install

```bash
npm install -g @proofai/mcp-server
```

## Configure Claude Code

Add to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "proofai": {
      "command": "proofai-mcp",
      "env": {
        "PROOFAI_API_KEY": "pk_live_xxx",
        "PROOFAI_ANON_KEY": "your-supabase-anon-key"
      }
    }
  }
}
```

## Tools

### `proofai_certify`
Certify an AI decision with cryptographic proof. Full pipeline in one call.

```
> Use proofai_certify to certify my analysis of this contract
```

### `proofai_log`
Log an AI decision that already happened (prompt + response you provide).

```
> Use proofai_log to record this decision with prompt "..." and response "..."
```

### `proofai_verify`
Verify a bundle's integrity and blockchain anchoring.

```
> Use proofai_verify to check bundle bnd_8019b37a7f44_1774735436195
```

### `proofai_polygonscan`
Get the Polygonscan URL for independent verification.

```
> Use proofai_polygonscan for tx 0xbbf92ceb6354a066...
```

### `proofai_monitor`
Get AI compliance monitoring stats (EU AI Act Article 72).

```
> Use proofai_monitor to check compliance status
```

## Why MCP?

Developers use Claude Code, not web dashboards. This MCP server brings AI compliance directly into the coding workflow:

- Every AI decision can be certified without leaving the terminal
- Verification is one tool call away
- Monitoring happens alongside development
- No context switching between coding and compliance
