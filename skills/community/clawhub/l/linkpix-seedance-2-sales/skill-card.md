## Description:

Guides ecommerce teams in creating short product showcase and advertising videos from product images and selling points using Seedance 2.0 through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce marketers, advertising creatives, and livestream teams use this skill to plan and generate short product videos from product images and selling points for online storefronts and ads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating npm tooling changes the local environment.

Mitigation: Review the qhkit package and installation instructions before allowing the agent to install or update it.

Risk: API credentials and selected product media are used by an external video-generation service.

Mitigation: Use a dedicated API token and upload only media approved for sharing with the service.

Risk: Submitting a generation task spends account credits and cannot be cancelled.

Mitigation: Check the model, duration, media, and estimated credits, then require explicit user approval before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-seedance-2-sales)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API key setup guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with command examples and video result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides task status, resulting video links, and charged credits when generation completes.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
