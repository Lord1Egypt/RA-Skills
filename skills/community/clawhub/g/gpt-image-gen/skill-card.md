## Description:

Generate images using ChatGPT's GPT-Image-2 model via browser automation, then extract the generated result from the browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate images through ChatGPT in an existing Brave browser session, refine prompts, poll for completion, extract the resulting image, and optionally send it to a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent broad control of an already-logged-in Brave browser session through remote debugging.

Mitigation: Use a dedicated browser profile or isolated automation browser and review actions before running the workflow.

Risk: Unsafe prompt-insertion instructions may mishandle untrusted prompt text.

Mitigation: Avoid untrusted prompt text until prompt encoding is fixed and review prompt contents before submission.

Risk: Generated media may be sent to an external Feishu destination.

Mitigation: Confirm the destination before sending generated media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayf3/skills/gpt-image-gen)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Image files]

**Output Format:** [Markdown guidance with bash and Python snippets; extracted generated image as a PNG file when execution succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in ChatGPT session in Brave with remote debugging on port 9222 and the websockets Python package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
