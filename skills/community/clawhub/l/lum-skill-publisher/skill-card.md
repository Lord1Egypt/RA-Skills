## Description:

Research, structure, and publish skills to ClawHub by analyzing top listings, generating gap reports, patching README/SKILL files, and guiding clawhub publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ragesaq](https://clawhub.ai/user/ragesaq)

### License/Terms of Use:


## Use Case:

Developers and skill authors use this agent skill to research ClawHub marketplace patterns, assess draft skills against publishing expectations, improve README/SKILL files, and prepare a publish command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested patches could introduce incorrect or misleading guidance into skill files.

Mitigation: Review generated patches before accepting them and scan the skill before deployment.

Risk: The guided publish workflow could publish with the wrong slug, version, changelog, or account.

Mitigation: Approve the final clawhub publish command only after confirming the slug, version, changelog, and account.

Risk: Research installs can pull marketplace skills into the local environment.

Mitigation: Keep research installs in a temporary directory.

## Reference(s):

- [ClawHub Skill Publisher Listing](https://clawhub.ai/ragesaq/skills/lum-skill-publisher)
- [ClawHub](https://clawhub.ai)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command blocks and suggested file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose README/SKILL.md changes and a final clawhub publish command; requires the clawhub CLI.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
