## Description:

Operates Kling AI through an OOMOL-connected account for video generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to submit Kling AI video generation jobs and retrieve their status and generated videos through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an unverified downloaded installer, and the external installers were unavailable for review.

Mitigation: Review and install a trusted oo CLI release yourself, and approve any additional installation or skill synchronization steps only after deciding they are acceptable.

Risk: Video generation requests pass through OOMOL and may consume credits.

Mitigation: Review the requested generation and expected credit use before submitting it, and monitor OOMOL billing.

## Reference(s):

- [Kling AI API documentation](https://app.klingai.com/global/dev/document-api/quickStart/productIntroduction/overview)
- [Kling AI](https://klingai.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [Shell commands with JSON request payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation runs asynchronously; responses include task status and generated video when available.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
