## Description: <br>
Configures Gmail sender-to-label routing through a local workflow that creates or reuses labels, creates filters, applies changes to existing messages, and can remove matching mail from INBOX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1u1s4](https://clawhub.ai/user/1u1s4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who manage Gmail accounts use this skill to route one or more senders into labels consistently, including existing messages and optional removal from INBOX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can make persistent Gmail routing changes, including creating labels and filters, applying labels to existing messages, and removing matching messages from INBOX. <br>
Mitigation: Run with --dry-run first, confirm the exact senders and label, and explicitly decide whether matching messages should stay in or leave INBOX. <br>
Risk: Using --replace-sender-filters can remove existing routing rules for a sender. <br>
Mitigation: Use --replace-sender-filters only when the user requests it or when duplicate/conflicting filters have been reviewed. <br>
Risk: The workflow requires Gmail access through local credentials and can manage labels, filters, and matching messages for the account. <br>
Mitigation: Install and run it only for accounts where the agent is intended to manage Gmail routing, and review credential scope and account context before execution. <br>


## Reference(s): <br>
- [Command Examples](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow reports created filters, deleted filters, retroactive message updates, label counts, and inbox counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
