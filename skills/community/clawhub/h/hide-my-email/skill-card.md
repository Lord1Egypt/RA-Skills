## Description:

Generate Apple Hide My Email addresses from the terminal and copy to clipboard.

This skill is for research and development only.

## Publisher:

[manikal](https://clawhub.ai/user/manikal)

### License/Terms of Use:

MIT

## Use Case:

Developers and macOS users use this skill to install and run the hme CLI for creating Apple Hide My Email aliases from an interactive terminal session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer paths can run or install unaudited code from an external GitHub repository.

Mitigation: Inspect the installer before use, avoid the curl-to-shell path, and verify the upstream repository and exact commit before running installation commands.

Risk: The tool requires broad macOS Accessibility permission for terminal-driven UI automation.

Mitigation: Grant Accessibility only after trusting the installed code and understanding that the permission allows the terminal to automate user interface actions.

Risk: Apple System Settings UI changes, rate limits, or non-interactive environments can break or block address generation.

Mitigation: Use on a supported interactive macOS session with iCloud+, expect manual troubleshooting, and avoid headless or SSH-only workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manikal/skills/hide-my-email)
- [Project homepage](https://github.com/manikal/hide-my-email)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and terminal output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI prints the generated masked email and copies the full address to the clipboard on success.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
