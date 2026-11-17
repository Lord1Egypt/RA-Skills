## Description:

Vision-driven browser automation using Midscene Bridge mode that operates from screenshots, connects to the user's desktop Chrome browser, and can interact with visible page elements while preserving browser session state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanru](https://clawhub.ai/user/quanru)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate browsing, data extraction, form interaction, screenshot capture, and UI validation in a real Chrome browser session. It is especially relevant when the task depends on cookies, login state, or page behavior visible only through the user's browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act through logged-in Chrome sessions and may operate on private, financial, administrative, or internal pages.

Mitigation: Review before use on sensitive sites and require explicit confirmation before actions that affect accounts, data, money, permissions, or administrative settings.

Risk: Visible page content and screenshots may be sent to configured AI model providers.

Mitigation: Configure only trusted providers and avoid using the skill on pages containing data that should not be shared with those providers.

Risk: The automation command uses a mutable npx package.

Mitigation: Prefer a pinned and reviewed Midscene package version before deployment.

## Reference(s):

- [Midscene.js](https://midscenejs.com)
- [Midscene Model Configuration](https://midscenejs.com/model-common-config)
- [Midscene Bridge Mode Documentation](https://midscenejs.com/bridge-mode-by-chrome-extension.html)
- [Midscene.js Chrome Extension](https://chromewebstore.google.com/detail/midscenejs/gbldofcpkknbggpkmbdaefngejllnief)
- [ClawHub Skill Page](https://clawhub.ai/quanru/skills/midscene-computer-chrome-bridge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown responses with inline shell commands, configuration examples, result summaries, and screenshot file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate screenshots and relies on configured visual model providers for browser state interpretation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
