## Description: <br>
Use this Lever skill for reading, creating, and updating Lever data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Lever connector schemas and operate Lever opportunities, postings, and opportunity notes through the oo CLI. It supports read actions and creating opportunity notes, with confirmation expected before write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change Lever opportunity records. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged [write]. <br>
Risk: A command may fail because the oo CLI is not installed, authentication is missing, the Lever connection is expired or incomplete, or billing blocks execution. <br>
Mitigation: Use the documented first-time setup steps only after the matching failure occurs, then retry the intended action. <br>
Risk: Connector inputs may drift from the static action descriptions. <br>
Mitigation: Fetch the live action schema with `oo connector schema` before constructing a payload. <br>


## Reference(s): <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Lever homepage](https://www.lever.co) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-lever) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
