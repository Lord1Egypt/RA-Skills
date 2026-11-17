## Description:

opencli浏览器自动化 helps agents control Chrome or Edge through opencli and a Browser Bridge extension for page navigation, screenshots, JavaScript evaluation, data extraction, and workflows on sites such as Zhihu, Bilibili, and Doubao.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxdwqy](https://clawhub.ai/user/wxdwqy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to automate browser workflows, inspect page state, capture screenshots, extract page content, and operate supported public or logged-in websites through opencli commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and operate an unverifiable browser extension.

Mitigation: Independently verify the extension source, version, permissions, and checksum before installation.

Risk: Automation can run against logged-in browser sessions and extract page text, screenshots, or structured data.

Mitigation: Use a dedicated browser profile with only the needed accounts, avoid sensitive sites, and limit extraction to data that is explicitly intended for the workflow.

Risk: Automating sites with anti-bot or verification controls can trigger account protections or violate platform expectations.

Mitigation: Do not use the skill to bypass anti-bot or verification controls, and require manual completion when a site presents verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxdwqy/skills/opencli-browser-automation)
- [Publisher profile](https://clawhub.ai/user/wxdwqy)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with opencli and PowerShell command examples plus JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires opencli, a compatible Chromium browser, and the Browser Bridge extension; outputs may reflect data visible in the active browser profile.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
