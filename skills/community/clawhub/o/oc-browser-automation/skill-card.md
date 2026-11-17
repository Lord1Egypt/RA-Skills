## Description:

浏览器控制工具 - 封装 OpenClaw browser 工具，支持网页自动化、截图、点击输入等操作

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control an OpenClaw browser session for web navigation, screenshots, DOM snapshots, clicking, typing, waiting, uploads, downloads, and browser debugging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser automation can act through logged-in pages or existing browser sessions.

Mitigation: Review target pages and session state before running actions, and avoid sharing browser state or screenshots that may contain sensitive data.

Risk: Upload, download, form submission, and optional Chrome profile actions can move local data or submit information to websites.

Mitigation: Confirm file paths, form contents, destination sites, and profile choice before executing actions that transfer data or use existing credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with browser command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation instructions and command snippets for agent execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
