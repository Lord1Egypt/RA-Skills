## Description:

睿观-版权检测 checks publicly accessible image URLs against a copyright-work database and returns similarity, rights-owner, TRO history, and radar-based risk indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, designers, and agents use this skill to assess whether an image may resemble registered copyrighted works before reuse. It supports copyright-risk screening, rights-owner lookup, TRO-history review, and factual reporting without giving legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends image URLs, uploaded local images, and API credentials to LinkFox/Ruiguan services.

Mitigation: Use only non-confidential images, confirm user consent before uploading local files, and store API keys in an appropriate credential store.

Risk: The security summary flags under-consented feedback reporting behavior.

Mitigation: Do not submit feedback unless the user has consented to the report content and destination.

Risk: Authentication and billing flows may involve phone verification, API key setup, account state, and payment orders.

Mitigation: Prefer self-service setup through the LinkFox agent console, avoid sharing phone or OTP values in chat when possible, and require explicit user approval before paid actions.

Risk: The skill writes full API responses and cache entries to local LinkFox session directories.

Mitigation: Review saved response files for sensitive image URLs or results and remove them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-ruiguan-copyright-detection)
- [API reference](references/api.md)
- [Onboarding and billing guide](references/onboarding.md)
- [LinkFox skills](https://skill.linkfox.com/)
- [LinkFox agent console](https://agent.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, JSON API responses saved to local files, and shell/configuration instructions for authentication, upload, and billing flows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detection calls require a public image URL or a local image uploaded to a temporary public URL; default results are cached for 24 hours and full responses are saved under a LinkFox session data directory.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
