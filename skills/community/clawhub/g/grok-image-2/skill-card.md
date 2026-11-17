## Description:

Generates images through Grok Imagine, guides saving the generated image locally, and can help send the selected file to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and workflow operators use this skill to automate image generation with Grok Imagine, save the resulting image, and optionally share the selected file to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate browser and desktop actions, read or copy local image files, and send a selected file to Feishu.

Mitigation: Install only if this automation scope is acceptable, and confirm the exact generated file path and intended recipient or channel before sending.

Risk: The artifact describes broad automation and sharing behavior without enough scoping or user confirmation.

Mitigation: Review each browser, desktop, and file-sharing action before execution; do not rely on artifact sandbox or whitelist wording as a technical guarantee.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/grok-image-2)
- [Grok Imagine](https://grok.com/imagine)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with JavaScript and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for browser and desktop automation, local image-file handling, and optional Feishu file sending.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
