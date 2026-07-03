## Description: <br>
Breathe (breathehr.com). Use this skill for Breathe requests that search or read account, employee, department, and location data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and agents use this skill to inspect Breathe HR data through the OOMOL `breathe` connector. It supports read-oriented account, employee, department, and location lookups while requiring schema inspection before building connector payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents a read-oriented workflow, but the connected account and connector may have broader authority than the listed read actions. <br>
Mitigation: Review available Breathe actions and account permissions before installation, and use an account whose Breathe permissions match the intended agent tasks. <br>
Risk: Future or newly available write, delete, or administrative actions could modify HR data if run without review. <br>
Mitigation: Require explicit user confirmation for any write, delete, or administrative change, including the exact target, payload, and expected effect. <br>


## Reference(s): <br>
- [Breathe homepage](https://www.breathehr.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-breathe) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke `oo connector schema` and `oo connector run` commands that return JSON from Breathe.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
