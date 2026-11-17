## Description:

Configure Chinese fonts for matplotlib plotting. Use when plotting charts with Chinese characters or getting garbled text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tazio7](https://clawhub.ai/user/tazio7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to configure and troubleshoot Chinese text rendering in Matplotlib charts, including font selection, Unicode minus handling, saved image output, and local font-cache reset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cache-clearing guidance can delete the user's local Matplotlib cache/config directory.

Mitigation: Confirm the Matplotlib cache path and user intent before running cache-clearing commands or scripts/clear_cache.py, especially in environments where Matplotlib cache paths may be redirected.

Risk: Font configuration may fail when the named Chinese font is not installed on the user's system.

Mitigation: List available fonts first and choose an installed font name before applying rcParams or fontname settings.

## Reference(s):

- [Troubleshooting Guide](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/tazio7/skills/matplotlib-chinese-font)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference bundled utility scripts for listing fonts, testing font rendering, and clearing the Matplotlib cache.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
