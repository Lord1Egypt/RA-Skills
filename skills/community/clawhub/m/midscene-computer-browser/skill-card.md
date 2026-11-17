## Description:

Vision-driven browser automation using Midscene that operates from screenshots, runs in headless Puppeteer by default, and can connect to an existing Chrome through CDP or Bridge mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanru](https://clawhub.ai/user/quanru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation agents use this skill to browse websites, collect data, fill forms, test browser UI behavior, take screenshots, and run multi-step web workflows through Midscene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in Chrome session through CDP or Bridge mode.

Mitigation: Prefer isolated headless Puppeteer mode or a dedicated Chrome profile, avoid unrelated logged-in tabs, and explicitly approve any CDP or Bridge use.

Risk: The skill runs the Midscene npm CLI with a mutable package tag.

Mitigation: Review the package before installation and consider pinning reviewed package versions instead of using mutable npm tags.

Risk: Browser automation can submit forms, click controls, or navigate pages in ways that affect user accounts or web applications.

Mitigation: Review planned actions before execution, use observable assertions for verification, and limit use to pages and sessions where the user has authorized automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quanru/skills/midscene-computer-browser)
- [Midscene.js](https://midscenejs.com)
- [Midscene Model Configuration](https://midscenejs.com/model-common-config)
- [Midscene Bridge Mode Documentation](https://midscenejs.com/bridge-mode-by-chrome-extension.html)
- [Midscene Chrome Extension](https://chromewebstore.google.com/detail/midscenejs/gbldofcpkknbggpkmbdaefngejllnief)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots, converted Midscene reports, extracted page data, and completion summaries.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
