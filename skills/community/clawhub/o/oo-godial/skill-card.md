## Description: <br>
GoDial (godial.cc). Use this skill for ANY GoDial request: reading, creating, and updating data through the OOMOL GoDial connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate GoDial through an OOMOL-connected account, including listing accounts and lists, reading contacts, and creating contacts in a selected list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected GoDial account and may use sensitive credentials through OOMOL. <br>
Mitigation: Connect only the GoDial account needed for the workflow and avoid broader permissions than the task requires. <br>
Risk: The create_contact action changes GoDial state by adding a contact to a target list. <br>
Mitigation: Confirm the target account, list, and complete contact payload with the user before running write actions. <br>
Risk: Connector action schemas can change over time, making stale payload assumptions unreliable. <br>
Mitigation: Inspect the live GoDial connector schema before building each action payload. <br>


## Reference(s): <br>
- [ClawHub GoDial skill](https://clawhub.ai/oomol/oo-godial) <br>
- [GoDial homepage](https://godial.cc) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
