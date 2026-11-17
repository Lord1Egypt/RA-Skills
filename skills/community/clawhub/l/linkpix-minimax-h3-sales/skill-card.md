## Description:

Guides agents in creating MiniMax H3 ecommerce videos from product images and prompts through the qhkit service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce marketers and video teams use this skill to plan, price, submit, and retrieve short product-promotion videos with synchronized audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setting up qhkit requires an API key that grants access to the user's account.

Mitigation: Use a trusted credential-handling method and avoid exposing the key in shared outputs.

Risk: Selected product images or video assets are uploaded to the service.

Mitigation: Confirm that the user is authorized to share each asset before uploading it.

Risk: Generating videos consumes credits and submitted tasks cannot be canceled.

Mitigation: Show the parameters and estimated charge, then wait for explicit user approval before submission.

Risk: Configuring a domestic account may overwrite an existing international-account setup.

Mitigation: Check the current account environment and confirm the intended account before changing configuration.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-minimax-h3-sales)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [qhkit API key setup guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and video result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimated and actual credit use, task status, and video URLs when available.]

## Skill Version(s):

0.1.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
