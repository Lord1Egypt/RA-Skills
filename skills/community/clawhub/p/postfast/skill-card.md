## Description:

Guides agents in scheduling and managing social media content, connected accounts, media uploads, and comments through PostFast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peturgeorgievv](https://clawhub.ai/user/peturgeorgievv)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, agencies, and developers use this skill to plan cross-platform posts, manage connected accounts and media, and handle comments with the PostFast service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing, replying, hiding, or deleting content may affect live social accounts immediately.

Mitigation: Confirm the action, account, content, and exact targets with the user before execution; inspect counts and filters for bulk deletion.

Risk: A leaked API key or account-connect link could grant unintended access to connected accounts.

Mitigation: Use the service only with a trusted workspace, keep the API key private, and share scoped connect links only with their intended recipients.

## Reference(s):

- [PostFast ClawHub release](https://clawhub.ai/peturgeorgievv/skills/postfast)
- [PostFast website](https://postfa.st)
- [API reference](references/api-reference.md)
- [Platform controls](references/platform-controls.md)
- [Media specifications](references/media-specs.md)
- [Upload flow](references/upload-flow.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON configuration]

**Output Format:** [Markdown with example API requests and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PostFast API key and connected social accounts for live actions.]

## Skill Version(s):

1.19.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
