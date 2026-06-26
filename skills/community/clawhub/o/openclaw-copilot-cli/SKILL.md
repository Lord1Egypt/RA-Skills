# copilot-cli

## Description
Execute GitHub Copilot CLI via exec for code gen, file edits, shell tasks using advanced models (Claude/GPT-5). Use when needing Copilot-powered coding/automation.

## Installation
```
npm install -g @github/copilot
```
or on macOS:
```
brew install copilot-cli
```

Verify:
```
copilot --help
```

## Authentication
1. Run `copilot` (interactive mode).
2. Type `/login` and follow prompts (uses GitHub account, requires Copilot subscription).

For non-interactive use after auth.

## Usage
### Non-interactive (one-shot prompts)
```
copilot -p \"Your prompt here\" --allow-all --silent
```
- `--allow-all`: Enables all tools/paths/URLs (use `--yolo` for short).
- `--silent`: Outputs only agent response.
- `--model claude-sonnet-4.6` or `gpt-5.2` etc. to choose model.

**In OpenClaw exec:**
```
exec:
  command: copilot -p 'Generate a Python script to...' --allow-all --silent
```

### Interactive
```
exec:
  command: copilot
  pty: true
```
Then use `process` tool:
- `send-keys`: Send input like `['prompt text', 'Enter']`
- `log`: View output

## Examples
### Shell task
```
copilot -p 'List all .js files and summarize' --allow-all
```

### Code generation
```
copilot -p 'Create a simple Express server in Node.js' --allow-all --silent
```

### File edits
```
copilot -p 'Add error handling to main.js' --allow-all
```

### Advanced models
```
copilot -p '...' --model gpt-5.3-codex --allow-all
```

## Test
Tested: Generated `hello_world.sh`:
```bash
#!/bin/bash
echo \"Hello, World!\"
```

Solana NFT mint test started successfully (complex task running).

## Tips
- Custom instructions from AGENTS.md auto-loaded.
- Use `--no-custom-instructions` if needed.
- For scripting: `--share` to output session.md
- Logs: `~/.copilot/logs/`