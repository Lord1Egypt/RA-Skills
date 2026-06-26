## Description: <br>
Agent Reach gives agents guidance for searching, reading, scraping, posting, and configuring access across web pages and social platforms including Twitter/X, Reddit, YouTube, GitHub, LinkedIn, RSS, and SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to help an agent retrieve online information, inspect supported platform URLs, run platform-specific search or read commands, and prepare channel setup steps. It is also used for guided posting or interaction workflows where the user has explicitly authorized the account action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward sensitive account, cookie, posting, and interaction workflows. <br>
Mitigation: Use isolated accounts and browser profiles, avoid raw cookie handling unless necessary, and require explicit user confirmation before login, cookie import, posting, commenting, proxy setup, or anti-bot browser workflows. <br>
Risk: External scraping and search requests may expose private or internal URLs to third-party services. <br>
Mitigation: Do not send private, internal, confidential, or access-controlled URLs through external scraping or search APIs. <br>
Risk: Persistent storage and platform credentials can extend access beyond a single session. <br>
Mitigation: Limit stored credentials to the minimum needed, keep persistent data in the documented user-scoped location, and remove credentials when the workflow is complete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/modesty-agent-reach) <br>
- [Project Homepage](https://github.com/Panniantong/Agent-Reach) <br>
- [Install Guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for SkillBoss API Hub workflows; some platform workflows may require cookies, login, proxy setup, or local CLI tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
