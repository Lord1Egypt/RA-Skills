## Description:

LLM Memory Integration provides memory-store and search interfaces, a SQLite FTS fallback implementation, and lifecycle hooks that can fetch a private enhancement package from CNB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xkzs2007](https://clawhub.ai/user/xkzs2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory CRUD and search capabilities to OpenClaw-style agents, with a safe SQLite FTS implementation available when the private enhancement package is not installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install-time hooks can clone mutable, unaudited code from the CNB endpoint into the skill directory.

Mitigation: Review the skill and remote CNB package before installation; disable hooks or require a pinned, signed, hash-verified package before enabling the private enhancement component.

Risk: The private enhancement package may introduce behavior beyond the public SQLite FTS fallback.

Mitigation: Use the public fallback implementation when trust in the private package is not established, and enable the private component only after reviewing its source and permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xkzs2007/skills/llm-memory-v8-fix)
- [Publisher profile](https://clawhub.ai/user/xkzs2007)
- [CNB private enhancement package endpoint](https://cnb.cool/llm-memory-integrat/llm)
- [Architecture documentation](docs/ARCHITECTURE.md)
- [Hooks documentation](hooks/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python interfaces and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local SQLite memory data and install a private package directory when hooks are enabled.]

## Skill Version(s):

8.0.1 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
