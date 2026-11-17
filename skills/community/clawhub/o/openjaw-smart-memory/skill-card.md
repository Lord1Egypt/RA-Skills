## Description:

Smart Memory gives an agent local JSON-backed persistent memory for storing, retrieving, updating, forgetting, exporting, and reporting on user preferences, facts, decisions, instructions, dates, and technical context without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and external agent users use Smart Memory to give an OpenClaw bot continuity across conversations by persisting local memories and retrieving relevant context before responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive personal facts, project details, standing instructions, and credentials in a local plaintext memory database.

Mitigation: Do not store API keys, passwords, tokens, or private infrastructure details; restrict permissions on ~/.openclaw/smart-memory before use.

Risk: Forget requests are implemented through soft deletion and archive retention before maintenance or purge removes data.

Mitigation: Verify forget, maintenance, archive retention, and purge behavior before relying on deletion guarantees.

Risk: Exports, statistics, and local JSON files may reveal sensitive memory contents or usage patterns.

Mitigation: Treat exported data, status reports, and all files under the memory directory as sensitive user data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcools1977/skills/openjaw-smart-memory)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; shell scripts output JSON and terminal text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON files under ~/.openclaw/smart-memory and requires jq.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
