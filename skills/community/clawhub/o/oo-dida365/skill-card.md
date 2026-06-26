## Description: <br>
Dida365 (dida365.com) skill for reading, creating, updating, and deleting Dida365 data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Dida365 tasks, projects, and habits through an OOMOL-connected account, including read, write, and delete workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive actions can change or remove Dida365 tasks, projects, or habit data. <br>
Mitigation: Confirm the exact payload, target identifiers, and user approval before running actions tagged write or destructive. <br>
Risk: Using the skill requires installing or signing into the OOMOL oo CLI and connecting a Dida365 account. <br>
Mitigation: Approve setup only when the user trusts OOMOL and intends to let an agent manage Dida365 data through that connection. <br>
Risk: Connector inputs may differ by action or change over time. <br>
Mitigation: Fetch the live action schema with the oo CLI before constructing each payload. <br>


## Reference(s): <br>
- [Dida365 homepage](https://dida365.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-dida365) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing JSON payloads; connector responses are JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
