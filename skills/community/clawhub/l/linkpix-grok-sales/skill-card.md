## Description:

Helps sellers create narrated product-promotion videos from product images and selling points through the Qinghu AI service, selecting an available model when Grok is not listed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and content teams use this skill to plan and generate short, narrated product videos for social-media marketing from product imagery and a brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed when shared in chat or commands.

Mitigation: Keep the token in a local environment variable or secret store rather than pasting it into chat.

Risk: Product images and other media are uploaded to a third-party service.

Mitigation: Use only media approved for upload and confirm trust in the qhkit/iqinghu service before submitting it.

Risk: Runtime package installation and video generation can introduce supply-chain exposure and consume credits.

Mitigation: Review and pin the npm package version; obtain approval for the estimated credit cost before generation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-grok-sales)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API key guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Video links]

**Output Format:** [Markdown with shell commands and links to generated videos]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation consumes service credits and requires user confirmation before submission.]

## Skill Version(s):

0.1.4 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
