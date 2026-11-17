## Description:

A stable native browser (WKWebView) for OpenClaw agents that opens a visible window with tab management, URL bar, and login helpers for sites including Perplexity, Grok, Claude, and ChatGPT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yungookim](https://clawhub.ai/user/yungookim)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to navigate and interact with websites through a visible native macOS browser, including authenticated web applications, form entry, screenshots, JavaScript execution, and multi-tab browsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions clone and install remote code without a pinned, reviewed commit.

Mitigation: Review the repository, pin a trusted commit before installation, and scan the code before enabling the skill.

Risk: The skill can handle authenticated browsing sessions, cookies, and website credentials.

Mitigation: Avoid hardcoding passwords, use separate or disposable browser profiles for sensitive accounts, and only use accounts appropriate for agent-driven browsing.

Risk: The skill recommends disabling built-in web search and fetch tools globally.

Mitigation: Keep built-in web tools enabled unless this replacement is intentional and the operational impact has been reviewed.

## Reference(s):

- [OpenClaw Native Browser ClawHub listing](https://clawhub.ai/yungookim/skills/openclaw-browser-2)
- [OpenClaw Browser repository](https://github.com/yungookim/openclaw-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code examples, JSON configuration, and API usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill operates a native macOS browser session and may persist cookies across invocations.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
