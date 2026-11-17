## Description:

Design UI screens in Paper, a local macOS design tool, by creating artboards, writing styled HTML, capturing screenshots, and iterating visually.

This skill is ready for commercial/non-commercial use.

## Publisher:

[candoolabs](https://clawhub.ai/user/candoolabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused agents use this skill to inspect and modify Paper design files on macOS, create UI artboards, insert styled HTML, and review screenshots during iterative interface design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configurable Paper MCP endpoint could connect the bridge to an untrusted server.

Mitigation: Use the default local Paper endpoint or set PAPER_MCP_URL only to a trusted local Paper server.

Risk: Screenshot saving and explicit save paths can write files to local storage, including sensitive or existing paths.

Mitigation: Use non-sensitive temporary paths, avoid --save for sensitive or existing files, and review generated files before sharing.

Risk: The workflow reads and modifies open Paper design files.

Mitigation: Install and run it only for trusted Paper workflows, and keep sensitive design files closed unless they are intended for editing.

## Reference(s):

- [Paper](https://paper.design)
- [Paper Design on ClawHub](https://clawhub.ai/candoolabs/skills/paper-design)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON arguments, and local screenshot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Paper running locally on macOS with curl and python3 available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
