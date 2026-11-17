## Description:

Guides brand and e-commerce teams through creating Seedance 2.5 product-promotion videos with Qinghu AI, from selecting a model and uploading media to estimating credits and delivering the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Brand teams, e-commerce designers, and advertisers use this skill to plan and generate short product-promotion videos from product images and selling points, review estimated credits, and retrieve the finished video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading the qhkit package introduces a third-party dependency.

Mitigation: Pin and review the package version before installation when supply-chain control is required.

Risk: API credentials and selected product media are supplied to the Qinghu service.

Mitigation: Use a dedicated API key, protect it from disclosure, and upload only media approved for sharing with the provider.

Risk: Video generation spends credits and submitted tasks cannot be canceled.

Mitigation: Show the model, media, duration, and estimated credits, then obtain explicit user approval before submitting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-seedance-25-sales)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key setup guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with commands, task status, and finished video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation consumes credits after user confirmation; delivery includes the video link and credits charged.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
