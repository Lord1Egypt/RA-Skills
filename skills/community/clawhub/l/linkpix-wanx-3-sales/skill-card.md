## Description:

Creates short e-commerce promotional videos from product images and selling points using Qinghu AI's Wanx video service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce merchants and operators use this skill to turn product images and selling points into short product showcase, promotion, and advertising videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance asks users to provide an API secret in chat.

Mitigation: Do not send API keys in chat; configure credentials through a secure local method such as the CLI's local configuration or an environment variable.

Risk: The security scan flags unpinned installation instructions, and its review was partial.

Mitigation: Review installation commands and assess whether unpinned packages are acceptable before installing; treat the partial scan as incomplete coverage.

## Reference(s):

- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-wanx-3-sales)

## Skill Output:

**Output Type(s):** [Video files, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Generated video files and task status results, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video duration, model, and media options depend on the available service choices.]

## Skill Version(s):

0.1.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
