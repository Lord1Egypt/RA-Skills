---
name: kimi-cli-doc-helper
description: |
  Answer Kimi Code CLI (kimi-cli) questions by querying and analyzing the official documentation at moonshotai.github.io/kimi-cli.
  
  TRIGGER CONDITIONS - Use this skill when:
  1. User directly asks about Kimi Code CLI / kimi-cli (installation, configuration, usage, commands, troubleshooting)
  2. User asks about terminal AI assistants for coding
  3. About to recommend or explain Kimi CLI configuration changes
  4. Answering questions where Kimi CLI is part of the solution
  
  MANDATORY: Always fetch relevant documentation from moonshotai.github.io/kimi-cli before:
  - Answering any Kimi CLI-specific question
  - Suggesting configuration changes
  - Providing technical details about Kimi CLI features
version: 1.0.0
author: 林霸天 (文轩先师の二弟子)
---

# Kimi CLI Documentation Helper

This skill helps answer Kimi Code CLI (kimi-cli) questions by automatically querying the official documentation at moonshotai.github.io/kimi-cli.

## When to Use

Use this skill when the user asks about:
- Kimi Code CLI installation and setup
- Configuration files and providers
- Available commands and options (`kimi`, `kimi web`, `kimi acp`)
- MCP (Model Context Protocol) configuration
- Troubleshooting issues
- Best practices for terminal AI coding assistants
- Any Kimi CLI-specific functionality

## Workflow

1. **Identify the query topic** - Understand what specific Kimi CLI topic the user is asking about

2. **Search/fetch relevant documentation** - Use `web_fetch` to retrieve documentation from moonshotai.github.io/kimi-cli:
   - For general questions: Start with `https://moonshotai.github.io/kimi-cli/en/`
   - For getting started: `https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html`
   - For configuration: `https://moonshotai.github.io/kimi-cli/en/configuration/config-files.html`
   - For MCP: `https://moonshotai.github.io/kimi-cli/en/customization/mcp.html`
   - For commands: `https://moonshotai.github.io/kimi-cli/en/reference/kimi-command.html`
   - For FAQ: `https://moonshotai.github.io/kimi-cli/en/faq.html`
   - Use `web_search` with site:moonshotai.github.io/kimi-cli if unsure where to look

3. **Analyze the documentation** - Read and understand the fetched content

4. **Formulate a comprehensive answer** - Based on the official documentation, provide an accurate response

5. **Cite sources** - Mention that the information comes from moonshotai.github.io/kimi-cli

## Key Documentation URLs

- Main docs: https://moonshotai.github.io/kimi-cli/
- English docs: https://moonshotai.github.io/kimi-cli/en/
- Getting Started: https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html
- Configuration: https://moonshotai.github.io/kimi-cli/en/configuration/config-files.html
- MCP Configuration: https://moonshotai.github.io/kimi-cli/en/customization/mcp.html
- Command Reference: https://moonshotai.github.io/kimi-cli/en/reference/kimi-command.html
- FAQ: https://moonshotai.github.io/kimi-cli/en/faq.html
- GitHub: https://github.com/MoonshotAI/kimi-cli

## Quick Reference

### Installation
```bash
# Linux / macOS
curl -LsSf https://code.kimi.com/install.sh | bash

# Windows (PowerShell)
Invoke-RestMethod https://code.kimi.com/install.ps1 | Invoke-Expression

# Or via uv
uv tool install --python 3.13 kimi-cli
```

### Usage Modes
- `kimi` - Interactive CLI
- `kimi web` - Browser UI
- `kimi acp` - Agent integration service

### Common Commands
- `/login` - Configure API provider
- `/init` - Generate AGENTS.md for project
- `/help` - Show all slash commands

## Example Usage

User: "How do I configure MCP in Kimi CLI?"

Action:
1. Fetch `https://moonshotai.github.io/kimi-cli/en/customization/mcp.html`
2. Analyze the MCP configuration documentation
3. Provide step-by-step instructions based on official docs

## Notes

- Always prefer official documentation over general knowledge
- If documentation is unclear or missing, say so and suggest checking the GitHub repo
- Keep answers concise but complete
- Kimi CLI is a product of Moonshot AI (月之暗面)
