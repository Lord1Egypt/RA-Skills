## Description:

Windows应用控制器 helps an agent control Windows desktop applications through Python automation, including launching and closing apps, clicking controls, filling forms, and taking screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to draft and run Windows GUI automation for application testing, data entry, repetitive desktop workflows, and screen-based control tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent high-impact control over a Windows desktop, including clicks, text entry, screenshots, app launches, and process termination.

Mitigation: Use it only in a controlled Windows session and require explicit confirmation before clicks, form submissions, application launches, or process termination.

Risk: Screenshots may expose sensitive windows or private information.

Mitigation: Close or hide sensitive windows before enabling screenshot-based workflows and review captured files before sharing them.

Risk: The artifact includes an unsafe taskkill/os.system process termination example.

Mitigation: Replace it with a safer subprocess or psutil implementation that validates process names and uses allowlists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-windows-controller)
- [ClawHub publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operation reports, dependency installation commands, automation script snippets, and screenshot file references.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
