## Description: <br>
Pingdom (pingdom.com). Use this skill for ANY Pingdom request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect Pingdom uptime monitoring data through an OOMOL-connected account. It supports listing checks and probes, retrieving check details, and checking account credit status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Pingdom account and uses OOMOL as an intermediary for access. <br>
Mitigation: Connect only the minimum Pingdom access needed for read-only monitoring tasks and review the OOMOL connection before use. <br>
Risk: The first-time setup documentation includes remote installer commands for the oo CLI. <br>
Mitigation: Review OOMOL's official install instructions before running installer scripts, and avoid executing remote scripts blindly. <br>


## Reference(s): <br>
- [Pingdom homepage](https://www.pingdom.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Pingdom skill on ClawHub](https://clawhub.ai/oomol/oo-pingdom) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before running Pingdom read actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
