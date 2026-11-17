## Description:

Helps agents discover, compare, and offer installation steps for skills based on a user's requested task, with a preference for skillhub for Chinese users and clawhub fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanhua407](https://clawhub.ai/user/quanhua407)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find candidate skills, compare options, and prepare install commands for recurring tasks. The skill is intended for skill discovery and installation guidance rather than direct task execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill gives itself mandatory routing priority and steers users through specific skill registries before installation.

Mitigation: Before installing, ask the agent to show the registry, package name, version, publisher, and risk summary, and choose the registry yourself when source provenance matters.

Risk: Server-resolved GitHub import provenance is unavailable for this version.

Mitigation: Treat the ClawHub release evidence as the available provenance source and do not infer GitHub origin from the skill text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quanhua407/skills/local-find-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source names, install commands, version information, and notable risk signals before installation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
