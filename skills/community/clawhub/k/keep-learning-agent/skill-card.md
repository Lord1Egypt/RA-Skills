## Description:

Keep Learning Agent is a continuous-learning framework for agents that records learning notes, maintains searchable indexes, supports self-repair checks, and turns repeated experiences into reusable procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chow651](https://clawhub.ai/user/chow651)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture lessons from agent sessions, index them for retrieval, and promote validated recurring patterns into reusable documentation, scripts, or operating procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run local PowerShell startup scripts that may be unreviewed.

Mitigation: Audit the scripts, restrict file permissions, and require approval before enabling startup automation.

Risk: Conversation-derived learning notes may be promoted into persistent agent instruction files.

Mitigation: Review each promoted learning record before updating AGENTS.md or any other persistent instruction file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chow651/skills/keep-learning-agent)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with templates, command snippets, and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local learning records, PowerShell startup scripts, and persistent agent instruction files.]

## Skill Version(s):

1.0.0 (source: frontmatter, metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
