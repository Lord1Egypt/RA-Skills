# Local access and MCP

## SSH tunnel patterns

Keep all GUI and REST listeners on the VPS bound to `127.0.0.1`. Reach them from the laptop only through SSH tunnels.

### noVNC plus REST

```bash
ssh -L 6081:127.0.0.1:6081 -L 3210:127.0.0.1:3210 root@<VPS_IP>
```

Then open:
- `http://localhost:6081/vnc.html?autoconnect=1&resize=scale`
- `http://localhost:3210`

### Native VNC

```bash
ssh -L 5902:127.0.0.1:5902 root@<VPS_IP>
```

Then connect a VNC client to `localhost:5902`.

Do not open `http://localhost:5902/`. That port speaks VNC, not HTTP.

## SSH config for the user laptop

Recommended `~/.ssh/config` entry:

```sshconfig
Host proxima-vps
  HostName <VPS_IP>
  User root
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

Passwordless SSH keys are strongly preferred. Many MCP IDE clients fail when an interactive password prompt appears.

Verify:

```bash
ssh proxima-vps 'echo OK'
ssh -T proxima-vps proxima-mcp
```

The second command often looks like it hangs after showing startup logs. That is normal for stdio MCP.

## MCP config snippets

### Antigravity

Agent Panel → Manage MCP Servers → View raw config:

```json
{
  "mcpServers": {
    "proxima-vps": {
      "command": "ssh",
      "args": ["-T", "proxima-vps", "proxima-mcp"]
    }
  }
}
```

### Windsurf

Usually `~/.codeium/mcp_config.json`:

```json
{
  "mcpServers": {
    "proxima-vps": {
      "command": "ssh",
      "args": ["-T", "proxima-vps", "proxima-mcp"]
    }
  }
}
```

### Zed

Add to `settings.json`:

```json
{
  "context_servers": {
    "proxima-vps": {
      "command": "ssh",
      "args": ["-T", "proxima-vps", "proxima-mcp"],
      "env": {}
    }
  }
}
```

## How to test from the IDE

Prompt the IDE agent explicitly to use the Proxima MCP server. Example:

```text
Use the `proxima-vps` MCP server and call `ask_chatgpt` with: "reply with exactly: MCP ChatGPT OK"
```

Then:

```text
Use the `proxima-vps` MCP server and call `ask_gemini` with: "reply with exactly: MCP Gemini OK"
```

If these succeed, the MCP path is healthy.

## Useful MCP tools often available

- `ask_chatgpt`
- `ask_claude`
- `ask_gemini`
- `ask_perplexity`
- `ask_all_ais`
- `compare_ais`
- `smart_query`
- `deep_search`
- `internet_search`
- `github_search`
- `security_audit`
- `review_code`
- `analyze_file`
- `fix_error`
- `write_tests`
- `new_conversation`

If an answer seems polluted by old chat state, call `new_conversation`.
