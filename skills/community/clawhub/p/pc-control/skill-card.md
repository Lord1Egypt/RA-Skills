## Description:

Remote Windows desktop control from WSL/Linux via screenshots plus mouse and keyboard simulation for GUI tasks that have no suitable CLI alternative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeron-g](https://clawhub.ai/user/zeron-g)

### License/Terms of Use:


## Use Case:

Developers and agents operating from WSL/Linux use this skill to inspect and control a Windows desktop when a GUI workflow has no practical command-line or PowerShell alternative.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can view and operate the user's Windows desktop, including visible sensitive information and active applications.

Mitigation: Run it only on a trusted local machine, close sensitive windows before use, and stop the server when finished.

Risk: Screenshots and authentication material may remain on disk after a session.

Mitigation: Delete leftover screenshot temporary files and the .auth_token file after use.

Risk: Mouse and keyboard automation can perform unintended actions if screen state or coordinates are wrong.

Mitigation: Take and review a screenshot after each action before continuing with further desktop control.

Risk: The security summary says the powerful desktop access is not tightly contained or cleaned up.

Mitigation: Prefer a version that pins dependencies, protects token storage, enforces timeouts, and reduces command-construction risk.

## Reference(s):

- [PC Control on ClawHub](https://clawhub.ai/zeron-g/skills/pc-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local screenshot file paths and structured action results while operating the desktop.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
