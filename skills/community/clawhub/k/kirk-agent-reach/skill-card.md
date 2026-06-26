## Description: <br>
agent-reach helps agents search, read, post, and interact across web and social platforms including Twitter/X, Reddit, YouTube, GitHub, WeChat, LinkedIn, Douyin, RSS, and arbitrary web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve information from supported web and social platforms, inspect URLs, run platform-specific search or read commands, and configure channels that require credentials or local setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use cookies and sensitive credentials that may act as active login sessions. <br>
Mitigation: Install only when the publisher and referenced external tools are trusted, avoid private URLs or confidential queries, and inspect or clear ~/.agent-reach after use. <br>
Risk: The skill includes posting, commenting, account, and setup actions across external platforms. <br>
Mitigation: Require explicit confirmation before any post, comment, account action, or persistent setup change. <br>
Risk: The security assessment marks the release suspicious because broad web access, scraping/search services, local storage, and action capabilities lack strong boundaries. <br>
Mitigation: Review the skill and its commands before deployment, constrain credentials to the minimum required platforms, and monitor resulting network and account activity. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kirkraman/kirk-agent-reach) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [Agent-Reach homepage](https://github.com/Panniantong/Agent-Reach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use external APIs, browser cookies, platform CLIs, local persistent storage under ~/.agent-reach, and temporary files under /tmp.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
