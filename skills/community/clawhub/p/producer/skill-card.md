## Description:

Guides agents in generating and editing AI music through AceDataCloud's Producer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to draft songs or lyrics, produce instrumentals, and edit existing audio using the Producer API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, audio IDs, and reference audio URLs are sent to AceDataCloud.

Mitigation: Avoid confidential or rights-sensitive material unless approved, and confirm you trust the publisher before use.

Risk: API calls can consume paid generation credits or expose an API key if mishandled.

Mitigation: Use a dedicated key with only needed APIs, keep it out of prompts and commits, monitor billing, and poll an existing task rather than submitting it again.

## Reference(s):

- [Producer Music on ClawHub](https://clawhub.ai/acedatacloud/skills/producer)
- [AceDataCloud API key setup](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud authentication guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud asynchronous task guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON API request examples]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio generation is asynchronous; check the returned task status before using results.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
