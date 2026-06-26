## Description: <br>
ClassMarker helps agents read ClassMarker groups, links, tests, and recent results through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect ClassMarker groups, links, assigned tests, and recent assessment results through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClassMarker groups, links, tests, and recent results may include sensitive assessment information. <br>
Mitigation: Install and use the skill only when the agent is intended to read ClassMarker data through the connected OOMOL account, and review outputs before sharing them. <br>
Risk: First-time setup may require installing the OOMOL CLI from a remote install command. <br>
Mitigation: Review the OOMOL CLI install command before running it, and use setup steps only after an auth, connection, or missing-CLI failure. <br>


## Reference(s): <br>
- [ClassMarker homepage](https://www.classmarker.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClassMarker skill on ClawHub](https://clawhub.ai/oomol/oo-classmarker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only ClassMarker connector actions and live action schemas before constructing requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
