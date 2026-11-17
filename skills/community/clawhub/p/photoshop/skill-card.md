## Description:

Control Adobe Photoshop from the shell via Flue - ExtendScript bridges without an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfkislev](https://clawhub.ai/user/sfkislev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill when a human asks an agent to inspect Photoshop state or make bounded edits inside Adobe Photoshop through Flue's shell-facing bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates Photoshop automation to local Flue instructions and adapter code that the security evidence describes as unaudited.

Mitigation: Review Flue and installed adapter documentation before use, and run only task-specific scripts in a constrained environment.

Risk: The artifact recommends an unpinned external setup command for Flue installation.

Mitigation: Use a pinned and verified Flue install, and require explicit human approval before setup or Photoshop-changing actions.

## Reference(s):

- [Flue project](https://github.com/SFKislev/flue)
- [Flue on PyPI](https://pypi.org/project/flue)
- [ClawHub Photoshop skill page](https://clawhub.ai/sfkislev/skills/photoshop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and ExtendScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When Flue is available, the skill guides an agent to send scripts through a Photoshop bridge and consume structured JSON results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
