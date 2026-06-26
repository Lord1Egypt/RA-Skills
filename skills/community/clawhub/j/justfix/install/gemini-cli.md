# Installing JustFix Skill on Gemini CLI

[Gemini CLI](https://github.com/google-gemini/gemini-cli) is Google's terminal-based AI assistant for developers. It supports MCP servers.

## Step 1: Register the MCP server

Edit `~/.config/gemini-cli/config.json` (create if it doesn't exist):

```json
{
  "mcp_servers": {
    "justfix-estimator": {
      "url": "https://estimator-mcp.justfix.app/mcp",
      "transport": "streamable-http"
    }
  }
}
```

Verify with:

```bash
gemini mcp list
```

You should see `justfix-estimator` listed.

## Step 2: Add the skill to your Gemini system instructions

Gemini CLI doesn't have a native skills folder, but you can include the SKILL.md content in your system instructions file:

```bash
mkdir -p ~/.config/gemini-cli/instructions
cd ~/.config/gemini-cli/instructions
git clone https://github.com/Just-Fix/justfix-skill.git justfix
```

Then reference it in `~/.config/gemini-cli/config.json`:

```json
{
  "system_instructions_include": [
    "~/.config/gemini-cli/instructions/justfix/SKILL.md"
  ],
  "mcp_servers": {
    "justfix-estimator": {
      "url": "https://estimator-mcp.justfix.app/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Step 3: Verify

```bash
gemini
```

Ask:

> How much would it cost to get a plumber out for 2 hours?

Gemini should call `service-estimate-card` with `service_code=plumbing`, `estimate=2` and return the quote.

## Notes

- Gemini CLI's MCP support is newer than Claude Code / Cursor. Confirm your Gemini CLI version supports streamable-HTTP transport with `gemini --version`.
- No auth required.
- Booking URL renders as plain text in the terminal.

## Updating

```bash
cd ~/.config/gemini-cli/instructions/justfix
git pull
```
