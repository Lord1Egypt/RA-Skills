## Description:

Integrate with the Max Studio API for image and video generation, uploads, task polling, media downloads, and batch result packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voidreal](https://clawhub.ai/user/voidreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external integrators use this skill to call Max Studio endpoints for media generation, uploads, task status polling, downloads, and batch result handling through a reusable Python CLI wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Max Studio API key and may require a Google access token, which are sent to a third-party service.

Mitigation: Use the skill only when you are comfortable sharing those credentials with Max Studio, use least-privilege or disposable credentials where possible, and rotate or revoke tokens after use.

Risk: Supplying secrets directly through shell command arguments can expose them through command history or process listings.

Mitigation: Avoid pasting real secrets into reusable shell history, prefer an isolated environment, and clear history or use safer secret handling before operational use.

Risk: The download command writes media from user-supplied signed URLs to local paths.

Mitigation: Restrict downloads to trusted media URLs and safe output directories.

Risk: The skill depends on the unpinned requests package.

Mitigation: Pin and review dependencies before operational deployment.

## Reference(s):

- [API Integration Guide - Max Studio](references/api_docs.md)
- [Max Studio API endpoint](https://max-studio.store)
- [Max Studio API key registration](https://max-studio.shop)
- [ClawHub skill page](https://clawhub.ai/voidreal/skills/max-studio-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Files]

**Output Format:** [Markdown guidance with shell commands, JSON API responses, generated media downloads, and optional packaged result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Max Studio API key and, for media endpoints, a user-provided Google access token.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
