## Description: <br>
Manage and read email through the mailbox CLI with structured JSON output for listing, showing, deleting, digesting, and monitoring messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeguooooo](https://clawhub.ai/user/leeguooooo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to inspect and manage mailbox content through explicit mailbox CLI commands while preserving structured success and error handling for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive mailbox data or change email state. <br>
Mitigation: Confirm mailbox-cli trust and account permissions before installation, and require explicit user approval before sending, deleting, monitoring, or otherwise changing email state. <br>
Risk: Email deletion is destructive. <br>
Mitigation: Use --dry-run before mutating when available, and require --account-id plus --confirm for destructive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeguooooo/mailbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with mailbox CLI command examples and JSON output expectations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automation should use --json and check success; mutating actions should use dry-run when available and require explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
