## Description: <br>
Baserow (baserow.io). Use this skill for ANY Baserow request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate connected Baserow accounts through the OOMOL oo CLI, including table discovery and row read, create, update, and delete workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates through a connected Baserow account and may use sensitive service credentials. <br>
Mitigation: Run it only with accounts and scopes appropriate for the task, and avoid privileged credentials unless they are required. <br>
Risk: Create and update actions change Baserow data. <br>
Mitigation: Confirm the exact table, row, payload, and expected effect with the user before running write actions. <br>
Risk: The delete action removes Baserow rows. <br>
Mitigation: Require explicit user approval for the target row before executing destructive deletion. <br>


## Reference(s): <br>
- [ClawHub Baserow skill page](https://clawhub.ai/oomol/oo-baserow) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Baserow homepage](https://baserow.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
