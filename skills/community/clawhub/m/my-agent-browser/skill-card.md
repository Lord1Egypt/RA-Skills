## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujiang817](https://clawhub.ai/user/liujiang817)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser workflows such as navigation, form filling, UI testing, structured page inspection, screenshots, recordings, and data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser sessions and page captures can contain credentials, cookies, personal data, or other secrets.

Mitigation: Save state only when necessary, keep state files private, delete them after use, and review screenshots, PDFs, videos, traces, and saved state before sharing.

Risk: Installing or updating the browser automation CLI from an unreviewed package version could introduce unwanted behavior.

Mitigation: Install from a trusted npm package version and pin to an exact reviewed release where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liujiang817/skills/my-agent-browser)
- [agent-browser CLI Project](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill Issues](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser state files, screenshots, PDFs, videos, and traces when the documented commands are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
