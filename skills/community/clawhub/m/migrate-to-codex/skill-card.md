## Description:

Migrate supported instruction files, skills, agents, and MCP config into Codex project and global files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to migrate Claude Code instructions, skills, agents, hooks, and MCP configuration into Codex-compatible project or global files. It guides inspection, dry-run migration, validation, and review of generated Codex artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent changes to Codex instructions, skills, agents, hooks, and configuration.

Mitigation: Run --scan-only, --plan, and --dry-run before writing, then manually review generated AGENTS.md, .codex/config.toml, .codex/hooks.json, .agents/skills, and .codex/agents files.

Risk: Server security evidence reports a path-containment flaw that can write or delete outside the selected target through symlinks.

Mitigation: Before using --replace or writing changes, inspect the target tree for symlinked .agents, .agents/skills, .codex, and .codex/agents paths.

## Reference(s):

- [Migration Differences](references/differences.md)
- [ClawHub Skill Page](https://clawhub.ai/eohmig/skills/migrate-to-codex)
- [Codex Configuration Reference](https://developers.openai.com/codex/config-reference)
- [Codex MCP](https://developers.openai.com/codex/mcp)
- [Codex Skills](https://developers.openai.com/codex/skills)
- [Codex Subagents](https://developers.openai.com/codex/subagents)
- [Codex Hooks](https://developers.openai.com/codex/hooks)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Claude Code Settings](https://code.claude.com/docs/en/settings)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with shell commands and generated or updated Codex configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent Codex project or global artifacts after scan, plan, and dry-run steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
