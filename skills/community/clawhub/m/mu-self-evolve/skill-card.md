## Description:

Helps AI agents turn conversation signals, errors, feedback, and decisions into local diaries, structured learning records, reviewed memory updates, and optional skill drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to maintain a local self-improvement loop for LLM agents, including daily experience capture, weekly error reflection, rule verification, memory cleanup, and draft skill synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically turn conversation-derived observations into persistent agent behavior or memory files.

Mitigation: Require explicit human approval before changes to MEMORY.md, SOUL.md, TOOLS.md, AGENTS.md, or newly synthesized skills.

Risk: Scheduled automation can run the evolution workflow without close supervision.

Mitigation: Review, adjust, or disable automatic cron setup before deployment, especially in shared or sensitive workspaces.

Risk: Error and conversation logging may capture tokens, API keys, URLs, parameters, cookies, or private payloads.

Mitigation: Add redaction rules for credentials and private data before writing errors, traces, or daily diary entries.

Risk: Skill drafts and promoted rules may encode incorrect or misleading guidance if the source records are incomplete.

Mitigation: Review and scan generated skill drafts and promoted rules before installation or use by other agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muippt/skills/mu-self-evolve)
- [File structure and domain tags](references/file-structure.md)
- [Record templates](references/record-templates.md)
- [Weekly reflection workflow](references/weekly-reflection.md)
- [Claude Code compatibility](references/claude-code-compat.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local Markdown or code files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write daily diaries, learning records, error records, feature request records, weekly narratives, archives, long-term memory updates, and optional skill draft files.]

## Skill Version(s):

3.1.0 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
