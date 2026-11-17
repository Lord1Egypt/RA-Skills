## Description:

Gmail: Read a message and extract its body or headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent in reading a specific Gmail message by ID and extracting either the body or selected headers through the gws CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gmail message bodies and headers can contain sensitive personal or business information.

Mitigation: Install and use this skill only when Gmail read access is intended, follow the shared gws authentication and security rules, and read only message IDs the user is authorized to inspect.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-gmail-read)
- [gws-shared](../gws-shared/SKILL.md)
- [gws-gmail](../gws-gmail/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can request text or JSON output, optional message headers, HTML body output, and dry-run command preview.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata; SKILL.md metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
