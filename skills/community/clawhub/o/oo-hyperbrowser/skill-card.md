## Description: <br>
Hyperbrowser lets agents use an OOMOL-connected Hyperbrowser account to fetch pages, search the web, and manage asynchronous web crawls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to browse, search, and retrieve structured Hyperbrowser results through an OOMOL-connected account. It supports read actions and user-confirmed crawl-start workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start Hyperbrowser crawl jobs through the user's connected account. <br>
Mitigation: Confirm the exact crawl payload and expected effect before running state-changing actions such as start_web_crawl. <br>
Risk: The skill requires an OOMOL-connected Hyperbrowser account and may use account credentials or billing credits. <br>
Mitigation: Connect only accounts and billing sources the user is comfortable letting the agent use, and stop for user action on authentication, connection, or billing errors. <br>


## Reference(s): <br>
- [ClawHub Hyperbrowser Skill](https://clawhub.ai/oomol/oo-hyperbrowser) <br>
- [Hyperbrowser Homepage](https://www.hyperbrowser.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before building action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
