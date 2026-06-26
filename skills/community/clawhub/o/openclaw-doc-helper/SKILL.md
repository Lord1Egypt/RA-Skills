---
name: openclaw-doc-helper
description: |
  Answer OpenClaw-related questions by querying and analyzing the official documentation at docs.openclaw.ai.
  
  TRIGGER CONDITIONS - Use this skill when:
  1. User directly asks about OpenClaw (configuration, usage, commands, troubleshooting, architecture)
  2. Suggesting OpenClaw as a solution to other problems
  3. About to recommend or explain OpenClaw configuration changes
  4. Answering questions where OpenClaw is part of the solution
  
  MANDATORY: Always fetch relevant documentation from docs.openclaw.ai before:
  - Answering any OpenClaw-specific question
  - Suggesting configuration changes
  - Providing technical details about OpenClaw features
version: 1.0.3
author: 文轩先师
---

# OpenClaw Documentation Helper

This skill helps answer OpenClaw-related questions by automatically querying the official documentation at docs.openclaw.ai.

## When to Use

Use this skill when the user asks about:
- OpenClaw configuration and setup
- Available commands and options
- Troubleshooting issues
- Architecture and design
- Best practices
- Any OpenClaw-specific functionality

## Workflow

1. **Identify the query topic** - Understand what specific OpenClaw topic the user is asking about

2. **Search/fetch relevant documentation** - Use `web_fetch` to retrieve documentation from docs.openclaw.ai:
   - For general questions: Start with `https://docs.openclaw.ai`
   - For specific topics: Try `https://docs.openclaw.ai/<topic>` (e.g., `/faq`, `/troubleshooting`, `/config`)
   - Use `web_search` with site:docs.openclaw.ai if unsure where to look

3. **Analyze the documentation** - Read and understand the fetched content

4. **Formulate a comprehensive answer** - Based on the official documentation, provide an accurate response

5. **Cite sources** - Mention that the information comes from docs.openclaw.ai

## Configuration Validation (User-Guided)

When suggesting configuration changes, guide the user to validate and view their configuration:

**Validate configuration:**

```bash
# Validate entire configuration
openclaw config validate
```

**View specific configuration sections:**

```bash
# View all plugins configuration
openclaw config get plugins

# View gateway settings
openclaw config get gateway

# View models configuration
openclaw config get models

# View channels configuration
openclaw config get channels

# View agents configuration
openclaw config get agents

# View specific channel (e.g., Feishu)
openclaw config get channels.feishu

# View nested values
openclaw config get agents.defaults.model.primary
openclaw config get channels.whatsapp.enabled
```

**Explain the validation output to the user:**
- If `valid: true` → configuration is correct, can proceed
- If errors → explain what needs to be fixed based on the error messages
- If warnings → inform user but note it's not blocking

## Key Documentation URLs

- Main docs: https://docs.openclaw.ai
- FAQ: https://docs.openclaw.ai/faq
- Troubleshooting: https://docs.openclaw.ai/troubleshooting
- Configuration: https://docs.openclaw.ai/config
- GitHub: https://github.com/openclaw/openclaw

## Example Usage

User: "How do I configure a new channel?"

Action:
1. Fetch `https://docs.openclaw.ai/config` or search for "channel configuration"
2. Analyze the configuration documentation
3. Provide step-by-step instructions based on official docs
4. Remind user to run `openclaw config validate` after making changes

## Notes

- Always prefer official documentation over general knowledge
- If documentation is unclear or missing, say so and suggest checking the GitHub repo
- Keep answers concise but complete
- **Security Note**: This skill does NOT execute any local commands. Users must run validation commands themselves.

## Safety & Security

This skill is **instruction-only** with no code execution:
- ✅ Only uses `web_fetch` and `web_search` tools
- ✅ Does NOT execute local commands or access files
- ✅ Does NOT require API keys or credentials
- ✅ Users retain full control over their system
