## Description: <br>
sevdesk (sevdesk.com). Use this skill for ANY sevdesk request: reading, creating, updating, and deleting data through the OOMOL sevdesk connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage sevdesk contacts through an OOMOL-connected sevdesk account. It supports reading contact records and, after confirmation, creating, updating, or deleting contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a connected sevdesk account and may access sensitive contact data. <br>
Mitigation: Install it only when you intend to let the agent use your OOMOL-connected sevdesk account. <br>
Risk: Write and delete actions can change or remove sevdesk contact records. <br>
Mitigation: Review confirmations carefully, especially contact identifiers and payload details, before allowing state-changing actions. <br>
Risk: First-time setup may require installing the oo CLI. <br>
Mitigation: Install the oo CLI only from the documented OOMOL source if prompted by an auth or connection failure. <br>


## Reference(s): <br>
- [sevdesk homepage](https://sevdesk.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-sevdesk) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payload construction; state-changing actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
