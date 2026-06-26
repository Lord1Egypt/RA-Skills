## Description: <br>
SerpApi lets agents run Google web, news, and Maps searches through an OOMOL-connected SerpApi account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search SerpApi-backed Google web, news, and Maps data without directly handling raw SerpApi API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup can require installing the oo CLI, signing in, connecting SerpApi credentials, or resolving billing before searches work. <br>
Mitigation: Review and approve each first-time setup, connection, credential, or billing step before it is performed. <br>
Risk: The skill requires sensitive credentials for SerpApi access through OOMOL. <br>
Mitigation: Use the OOMOL-mediated connector flow so raw SerpApi tokens are not handled directly by the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-serpapi) <br>
- [SerpApi homepage](https://serpapi.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to inspect the live connector schema before constructing each SerpApi action payload.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
