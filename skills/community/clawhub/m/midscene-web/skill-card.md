## Description:

Vision-driven browser automation using Midscene for browsing, scraping, form interaction, screenshots, and UI QA from page screenshots, with Puppeteer, CDP, and Bridge modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengzuo613](https://clawhub.ai/user/zengzuo613)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to navigate, inspect, test, and interact with web pages when visible browser state, screenshots, data extraction, or an existing Chrome session is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control browser pages and may operate against authenticated Chrome sessions in CDP or Bridge mode.

Mitigation: Prefer isolated Puppeteer mode for ordinary browsing and testing; use CDP or Bridge only after explicitly deciding to expose the real Chrome session.

Risk: The skill invokes mutable npm packages for browser automation.

Mitigation: Pin Midscene package versions and run the skill in a controlled environment for reviewed deployments.

Risk: Vision-grounded browser automation can misread visible state or act on the wrong page element.

Mitigation: Inspect screenshots before actions, use assertions after important steps, and review results before sensitive or irreversible browser operations.

## Reference(s):

- [Midscene.js](https://midscenejs.com)
- [Midscene Model Configuration](https://midscenejs.com/model-common-config)
- [Midscene Bridge Mode Documentation](https://midscenejs.com/bridge-mode-by-chrome-extension.html)
- [Midscene Chrome Extension](https://chromewebstore.google.com/detail/midscenejs/gbldofcpkknbggpkmbdaefngejllnief)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with shell commands, configuration snippets, status summaries, and optional generated browser artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots and Midscene report files when browser automation commands are executed.]

## Skill Version(s):

26.5.14 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
