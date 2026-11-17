## Description:

Create and deploy a festive Chinese New Year (Year of the Horse 2026) animated GIF sticker maker web app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafar](https://clawhub.ai/user/jiafar)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to scaffold a festive Next.js web app that generates custom Year of the Horse blessing cards and WeChat-compatible animated GIF stickers from user-provided text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public Google AI-backed endpoints can consume the installer's API quota.

Mitigation: Add authentication, rate limiting, and spend limits before deploying with real Google API keys.

Risk: User-submitted names and sticker text may be sent to Google AI services without enough disclosure.

Mitigation: Add provider disclosure and a privacy notice before collecting or processing user text.

Risk: Dependency integrity is weaker without a lockfile and with runtime loading of gif.js from a CDN.

Mitigation: Use a lockfile or npm ci, and bundle or self-host gif.js with integrity controls.

Risk: Unused AI endpoints increase cost and exposure if the deployment only needs local GIF sticker generation.

Mitigation: Remove unused AI routes and related environment variables when deploying only the local sticker maker.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiafar/skills/horse-sticker-maker)
- [gif.js](https://github.com/jnordberg/gif.js)
- [Google AI Platform model endpoint](https://aiplatform.googleapis.com/v1/publishers/google/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and a Next.js template project]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a reusable web app template for PNG blessing cards and animated GIF sticker generation.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
