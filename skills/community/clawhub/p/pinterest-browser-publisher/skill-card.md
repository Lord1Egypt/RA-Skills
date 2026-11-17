## Description:

Automate Pinterest pin publishing via browser automation with Playwright, including cookie-based sessions, single-pin publishing, carousel-style image inputs, and batch publishing for jp.pinterest.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoboask](https://clawhub.ai/user/luoboask)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and developers can use this skill to prepare and publish Pinterest pins from local image assets through browser automation when the Pinterest API is not used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored Pinterest cookies can act as login secrets if exposed.

Mitigation: Treat ~/.config/pinterest/cookies.json as sensitive, avoid sharing logs that may contain cookie details, and delete or rotate cookies after use.

Risk: Automation can publish content under a real Pinterest account.

Mitigation: Use only an account approved for automation and review configured pins before running auto-publish scripts.

Risk: The skill depends on local Node.js and Playwright execution.

Mitigation: Install dependencies in an isolated user environment and prefer pinned or locally reviewed dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoboask/skills/pinterest-browser-publisher)
- [ClawHub homepage metadata](https://clawhub.ai/skills/pinterest-browser-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser automation logs and screenshots while running publisher scripts.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and package.json report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
