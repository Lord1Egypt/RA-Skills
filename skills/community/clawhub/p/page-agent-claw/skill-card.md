## Description:

Uses a local page-agent service at http://localhost:4222 to run browser automation tasks such as opening pages, performing page actions, and extracting information when an agent needs browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucasytoo](https://clawhub.ai/user/ucasytoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to route browser-control requests through a locally running page-agent-claw service and Chrome extension. It is intended for explicit tasks such as opening sites, interacting with pages, searching, and extracting page information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local service receives broad free-form browser automation tasks and can control the user's browser through the connected extension.

Mitigation: Use the skill only for explicit browser-automation tasks, keep sensitive account workflows and secrets out of prompts, and confirm the browser action scope before execution.

Risk: The workflow depends on a globally installed npm package, a local service, and a Chrome extension.

Mitigation: Install only from trusted sources, pin and audit the page-agent-claw package where possible, and run the local service only when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucasytoo/skills/page-agent-claw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm, Node.js, curl, a local page-agent-claw service on port 4222, and the page-agent Chrome extension.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
