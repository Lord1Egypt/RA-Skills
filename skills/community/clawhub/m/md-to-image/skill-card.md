## Description:

Convert Markdown files into high-contrast, mobile-friendly PNG images optimized for Telegram and social media sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowhere1975](https://clawhub.ai/user/nowhere1975)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn trusted Markdown notes or posts into readable mobile PNG images for Telegram and social media sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill renders Markdown in a live browser without blocking embedded scripts or network requests.

Mitigation: Install only for Markdown files you trust; avoid untrusted Markdown until JavaScript is disabled, network requests are blocked, and raw HTML is sanitized.

Risk: Generated outputs are written to a shared temporary output location.

Mitigation: Use a private per-run output directory before processing sensitive content.

## Reference(s):

- [MD to Mobile Image on ClawHub](https://clawhub.ai/nowhere1975/skills/md-to-image)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image file with CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 1080px-wide PNG images and reports the generated file path.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
