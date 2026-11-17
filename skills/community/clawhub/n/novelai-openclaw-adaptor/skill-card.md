## Description:

Explain how to connect NovelAI to OpenClaw through a local OpenAI-compatible shim.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askkumptenchen](https://clawhub.ai/user/askkumptenchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure a local NovelAI adaptor, choose supported text or image models, and connect OpenClaw to a local OpenAI-compatible endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may install or run an unverified adaptor package.

Mitigation: Verify the package source, maintainer, repository, and release version before installation; prefer a trusted local checkout or pinned reviewed release.

Risk: NovelAI credentials could be exposed through chat or shell history.

Mitigation: Enter credentials only through the local configuration flow and never paste secrets into chat or inline shell commands.

Risk: Local configuration may point OpenClaw at the wrong endpoint or model.

Mitigation: Set OpenClaw base_url to the local adaptor endpoint and select an adaptor-supported text or image model before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/askkumptenchen/skills/novelai-openclaw-adaptor)
- [Publisher Profile](https://clawhub.ai/user/askkumptenchen)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers local setup guidance, model selection, credential-handling cautions, and OpenClaw base_url configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
