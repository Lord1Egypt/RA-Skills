## Description: <br>
Use this skill for Intercom requests involving reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, support operators, and developers use this skill to inspect Intercom admins, contacts, conversations, and workspace metadata through an OOMOL-connected Intercom workspace. It also helps create or update contacts and manage conversation replies, closing, and reopening when the user confirms the intended write action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can create or update contacts and change conversation state in Intercom. <br>
Mitigation: Confirm the exact target, payload, and intended effect with the user before running create, update, reply, close, or reopen actions. <br>
Risk: The skill depends on OOMOL's oo CLI and an OOMOL-connected Intercom workspace. <br>
Mitigation: Install only when the operator trusts the OOMOL CLI and is comfortable connecting the workspace through OOMOL. <br>
Risk: Action input fields may change with the live Intercom connector contract. <br>
Mitigation: Fetch the action schema with `oo connector schema` before constructing or running each payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-intercom) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Intercom homepage](https://www.intercom.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns Intercom connector responses as JSON when commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
