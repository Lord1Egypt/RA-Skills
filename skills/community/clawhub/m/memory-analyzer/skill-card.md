## Description:

Analyzes conversation history, extracts user preferences and feedback, and updates memory files automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tevfikgulep](https://clawhub.ai/user/tevfikgulep)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to analyze conversation history for user preferences, feedback patterns, and memory updates. It is intended to help maintain persistent agent memory and behavior files from reviewed session context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation history may contain personal identifiers or sensitive preference data.

Mitigation: Remove personal identifiers before installation and limit analysis to explicitly approved transcripts.

Risk: Automatic memory and agent-rule changes can persist incorrect, unwanted, or overly personal behavior.

Mitigation: Change the workflow to propose reviewed updates instead of directly modifying MEMORY.md, AGENTS.md, USER.md, IDENTITY.md, or SOUL.md.

Risk: Broad feedback triggers can turn casual statements into durable user preferences.

Mitigation: Narrow activation to explicit user approval or clearly labeled preference-update requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tevfikgulep/skills/memory-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown-formatted analysis and proposed memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include persistent-memory and agent-rule file changes when run without review.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
