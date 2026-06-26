## Description: <br>
Operate Capsule CRM through an OOMOL-connected account for reading, creating, updating, deleting, listing, and searching CRM records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to let an agent work with Capsule CRM records through OOMOL, including parties, opportunities, tasks, and CRM reference data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and delete actions can change or remove Capsule CRM records. <br>
Mitigation: Confirm the exact action, target record, and payload with the user before running create, update, or delete operations. <br>
Risk: The skill requires access to a Capsule CRM account through OOMOL and may use sensitive credentials. <br>
Mitigation: Install it only when the agent should access Capsule CRM through OOMOL, and rely on the server-side credential injection described by the release evidence. <br>
Risk: The optional oo CLI installation command downloads and runs a remote installer. <br>
Mitigation: Run the installer only when the CLI is missing and after reviewing OOMOL's official installation guidance. <br>


## Reference(s): <br>
- [ClawHub Capsule CRM Skill](https://clawhub.ai/oomol/oo-capsule-crm) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Capsule CRM Homepage](https://capsulecrm.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions return JSON responses when run through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
