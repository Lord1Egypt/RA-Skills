## Description: <br>
LinkedIn (linkedin.com). Use this skill for LinkedIn requests including reading, creating, updating, and deleting data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate LinkedIn through the OOMOL `oo` CLI after the user has connected a LinkedIn account. It supports schema-first execution for profile lookup, post creation, reshares, and post deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create posts, reshares, and delete LinkedIn posts through a connected account. <br>
Mitigation: Confirm the exact payload and expected effect with the user before write actions, and require explicit approval before destructive deletion. <br>
Risk: The skill depends on OOMOL account connectivity and server-side credential handling. <br>
Mitigation: Install and use it only when the user trusts OOMOL and intends to let an agent operate the connected LinkedIn account. <br>
Risk: First-time setup includes CLI installation commands that fetch remote install scripts. <br>
Mitigation: Prefer official or verified installation steps and review installation commands before running them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-linkedin) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [LinkedIn](https://www.linkedin.com) <br>
- [Skill Icon](https://static.oomol.com/logo/third-party/linkedin.png) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution; `oo connector run` responses include `data` and `meta.executionId`.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
