---
name: kilocode
description: AI coding agent CLI tool for generating code from natural language, automating tasks, and running terminal commands. Use when user wants to perform coding tasks, generate code, refactor, debug, or automate development workflows via CLI. Supports 500+ AI models via Kilo provider.
---

# Kilocode

Kilocode is an AI coding agent CLI tool that generates code from natural language, automates tasks, and runs terminal commands.

## Basic Usage

Run in any project directory:

```bash
kilo
```

### Non-interactive mode

Execute a single prompt without entering interactive REPL:

```bash
kilo run '<prompt>'
```

Continue previous conversation:

```bash
kilo run --continue '<prompt>'
```

Fully autonomous mode (CI/CD, no prompts):

```bash
kilo run --auto '<prompt>'
```

## Common Commands

| Command                        | Description                             |
| ------------------------------ | --------------------------------------- |
| `kilo`                         | Start interactive REPL                  |
| `kilo run "prompt"`            | Execute single prompt                   |
| `kilo run --continue "prompt"` | Continue with previous context          |
| `kilo run --auto "prompt"`     | Autonomous mode (no permission prompts) |
| `kilo --help`                  | Show help                               |

## Examples

### Generate code

```bash
kilo run "Create a Python function to calculate fibonacci sequence with memoization"
```

### Debug

```bash
kilo run "Fix the bug in index.js where the async function returns undefined"
```

### Refactor

```bash
kilo run "Refactor the React component to use hooks instead of class"
```

### Run terminal commands

```bash
kilo run "Run npm test and fix any failing tests"
```

### CI/CD automation

```bash
kilo run --auto "Run linting, tests, and build the project"
```

## Models

Kilocode supports 500+ AI models via the Kilo provider (configured in auth-profiles). Popular models:

- **Gemini 3.1 Pro** (default, fast)
- **Claude 4.6 Sonnet & Opus** (high quality)
- **GPT-5.2** (OpenAI)

Model selection is handled automatically based on provider configuration. No need to specify model unless required.

## Tips

- Use `--auto` flag only in trusted environments (CI/CD)
- Provide clear, specific prompts for better results
- Kilo can read and write files, run commands, and interact with browser
- Check [kilo.ai](https://kilo.ai) for documentation and updates
