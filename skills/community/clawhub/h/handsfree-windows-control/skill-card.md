## Description:

Guides agents in using the handsfree-windows CLI to automate native Windows UIA controls, browser actions, and mixed YAML macros.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinlar](https://clawhub.ai/user/lijinlar)

### License/Terms of Use:


## Use Case:

Developers and testers use this skill to control Windows desktop applications and browsers through the handsfree-windows CLI for UI discovery, interaction, screenshots, and YAML macro recording or replay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup installs mutable unpinned external code and dependencies at runtime, including browser binaries when browser automation is enabled.

Mitigation: Install only in a trusted, non-admin isolated Python environment or VM, review the external repository before setup, and use --no-browser unless browser automation is required.

Risk: Browser automation creates persistent profiles and session state that may retain cookies, login sessions, screenshots, or visited URLs.

Mitigation: Use dedicated automation accounts and browser profiles, review screenshots and recorded macros before sharing, and clear ~/.handsfree-windows when stored session state is no longer needed.

Risk: Broad desktop and browser control can trigger unintended actions in native applications or websites.

Mitigation: Inspect UI controls before acting, prefer selectors over coordinates, avoid typing credentials, and require human confirmation before destructive or submission actions.

## Reference(s):

- [handsfree-windows CLI reference](references/api_reference.md)
- [Handsfree Windows Control release page](https://clawhub.ai/lijinlar/skills/handsfree-windows-control)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with PowerShell commands and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the CLI to create screenshots, browser profiles, browser state, and macro files during agent use.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
