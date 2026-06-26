---
name: key-guard
description: "Security guardrail: prevents API keys from being sent to Claude. Triggers when user asks to call an external API, use a key, check credentials, read .env files, or view/edit scripts that may contain hardcoded keys. Always routes key usage through the local MCP server instead."
---

# Key Guard

A security skill that ensures API keys stay local and are never sent to Claude.

## When This Skill Applies

Activate whenever the user wants to:
- Call an external API (OpenAI, DeepL, Oxford Dictionary, etc.)
- Check if an API key is configured
- Read `.env`, `*.key`, `secrets.*`, or any credentials file
- View or edit a script (`.sh`, `.bash`, curl commands, config files) that may contain a hardcoded API key
- Debug why an API call is failing

## Rules (ALWAYS follow these)

1. **NEVER read `.env` or key files directly** — do not use bash `cat .env` or file read tools on any file containing keys
2. **NEVER read script or config files directly** if they might contain hardcoded API keys — use `read_file_masked` instead
3. **NEVER include a key value in your response**, even partially
4. **ALWAYS use the `key-guard` MCP server** for anything key-related

## How to Use the MCP Server

The `key-guard` MCP server exposes five tools:

### Tool 1: `list_keys`
Discover all available key names — never values.
```
Call: list_keys()
Returns: { keys: ["KEY_A", "KEY_B", "KEY_C"] }
```

### Tool 2: `validate_key`
Check if a key is configured without seeing it.
```
Call: validate_key({ key_name: "OPENAI_API_KEY" })
Returns: { exists: true, length: 51, preview: "sk-a****", message: "Key is set" }
```

### Tool 2: `call_api`
Make an authenticated HTTP request locally. The key is injected by the MCP server — Claude only sees the API response.
```
Call: call_api({
  key_name: "OPENAI_API_KEY",
  url: "https://api.openai.com/v1/models",
  method: "GET"
})
Returns: { status: 200, data: { ... API response ... } }
```

### Tool 3: `read_file_masked`
Read a script or config file with all key values replaced by `{{KEY_NAME}}` placeholders. Use this instead of reading files directly.
```
Call: read_file_masked({ file_path: "./call.sh" })
Returns: {
  content: "curl -H 'Authorization: Bearer {{OPENAI_API_KEY}}' https://..."
}
```
You can now safely view and suggest edits to the non-key parts.

### Tool 4: `write_file_with_keys`
Write a file back after editing, with `{{KEY_NAME}}` placeholders substituted with real key values locally.
```
Call: write_file_with_keys({
  file_path: "./call.sh",
  content: "curl -H 'Authorization: Bearer {{OPENAI_API_KEY}}' https://api.openai.com/v1/chat/completions ..."
})
Returns: { success: true, message: "File written with keys substituted locally" }
```

## Setup Instructions (tell the user if MCP is not running)

If the MCP server hasn't been registered yet:

```bash
# Clone the repo
git clone https://github.com/your-username/key-guard.git

# Copy .env.example to .env and fill in your keys
cp .env.example .env

# Register the MCP server (run once) — replace the path with your actual clone location
/mcp add key-guard node /path/to/key-guard/key-guard.js

# Or add directly to ~/.copilot/mcp-config.json for auto-load on restart:
# {
#   "mcpServers": {
#     "key-guard": {
#       "command": "node",
#       "args": ["/path/to/key-guard/key-guard.js"]
#     }
#   }
# }
```

## Example Workflows

### User: "Is my OpenAI key set up?"
```
1. Call validate_key({ key_name: "OPENAI_API_KEY" })
2. Report back: "Yes, your key is set (51 chars, starts with sk-a****)"
```

### User: "Call the OpenAI API to get word definitions"
```
1. Call call_api({
     key_name: "OPENAI_API_KEY",
     url: "https://api.openai.com/v1/chat/completions",
     method: "POST",
     body: { model: "gpt-4o-mini", messages: [...] }
   })
2. Use the returned response — never the key itself
```

### User: "Show me my .env file"
```
Do NOT read .env directly.
Instead, call validate_key for each expected key name and show:
- Which keys are configured
- Approximate length (as a sanity check)
Never show actual values.
```

### User: "Edit my curl script to add a header"
```
1. Call read_file_masked({ file_path: "./call.sh" })
   → Claude sees "curl -H 'Authorization: Bearer {{OPENAI_API_KEY}}' ..."
2. Make the requested edit to the non-key parts
3. Call write_file_with_keys({ file_path: "./call.sh", content: "<edited content with {{OPENAI_API_KEY}} still in place>" })
   → MCP substitutes the real key before writing to disk
```
