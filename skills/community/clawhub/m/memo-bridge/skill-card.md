## Description:

MemoBridge helps agents export, import, back up, migrate, and transfer AI memory or context between supported AI tools, including CodeBuddy, OpenClaw, Hermes Agent, Claude Code, Cursor, ChatGPT, Doubao, and Kimi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonelake](https://clawhub.ai/user/gonelake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI tool users use this skill to preserve and move assistant memory, preferences, project context, and workspace notes when switching tools, sharing context, or setting up a new environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles broad private AI context and may expose sensitive memories if exported content is shared without review.

Mitigation: Review the generated memo-bridge.md before sharing it and keep exported memory files in trusted storage.

Risk: Imported content can be written into persistent agent memory files.

Mitigation: Use --dry-run and explicit --workspace paths before importing, and manually inspect untrusted input for sensitive or instruction-like content.

Risk: Broad directory scanning may collect more context than intended.

Mitigation: Prefer explicit workspace paths and avoid auto-scanning broad directories unless the scope has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gonelake/skills/memo-bridge)
- [Publisher profile](https://clawhub.ai/user/gonelake)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated memory migration content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or consumes a memo-bridge.md interchange file and may generate paste-ready import or export instructions for prompt-guided tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
