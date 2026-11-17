## Description:

Maintains a SkillHub knowledge graph by adding, deleting, and replacing atomic notes to improve knowledge linking and retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain local SkillHub knowledge-graph notes under life/areas/**, including adding, deleting, replacing, and retrieving atomic notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests write access and potential command execution without clear operational boundaries.

Mitigation: Limit use to the intended life/areas/** notes, review proposed changes and commands before execution, and back up important files first.

Risk: The skill references API key configuration without clearly identifying the service that needs the key.

Mitigation: Avoid providing API keys unless the publisher clarifies what service uses them and why; keep any keys in environment variables and out of version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/graph-knowledge-base)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like status output with optional shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose changes to local knowledge-graph notes and environment configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
