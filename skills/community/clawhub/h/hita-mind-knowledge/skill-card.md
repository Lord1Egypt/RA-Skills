## Description:

Hita-Mind & Knowledge gives agents local CLI-accessible memory and knowledge stores for preferences, decisions, lessons, skills, methods, and rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hita126](https://clawhub.ai/user/hita126)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to let a Node.js-based agent save, search, and assemble long-term memory and reusable knowledge context across local JSON stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive conversation-derived memory or knowledge in local JSON stores.

Mitigation: Use explicit user-approved writes, avoid secrets and regulated personal data, and inspect or prune the stores regularly.

Risk: Retrieved memory or knowledge may replay stale, incorrect, or untrusted content into an agent context.

Mitigation: Treat retrieved entries as reference text for review rather than as instructions to follow automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hita126/skills/hita-mind-knowledge)
- [Publisher profile](https://clawhub.ai/user/hita126)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [CLI text and Markdown-style context assembled from JSON stores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists memory and knowledge records in local JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
