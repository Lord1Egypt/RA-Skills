## Description:

Agent Reach helps agents search, read, and interact with web pages and supported platforms including X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, Weibo, WeChat Articles, LinkedIn, Instagram, RSS, and SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use Agent Reach to search and read URLs or platform content, retrieve transcripts and feed data, configure channels, and, with explicit approval, post or interact through supported authenticated platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, URLs, and scraped content may be sent to external services.

Mitigation: Confirm before submitting sensitive URLs, private content, credentials, or confidential queries to external services.

Risk: Authenticated platform actions can use cookies or accounts to post, comment, or interact.

Mitigation: Require explicit user confirmation before cookie import, browser-cookie extraction, posting, commenting, or other account-changing actions.

Risk: Setup guidance may involve package installation, Docker, proxy configuration, or fetched remote install instructions.

Mitigation: Review commands and remote setup instructions before execution, and run only approved installation or configuration steps.

## Reference(s):

- [Agent Reach homepage](https://github.com/Panniantong/Agent-Reach)
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code and shell-command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API requests, command invocations, setup steps, and posting guidance that require user confirmation.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
