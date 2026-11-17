## Description:

Routes Gmail messages from specified senders to a target label by creating or reusing a label, creating a sender filter, applying changes to existing mail, and optionally removing matching messages from the Inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1u1s4](https://clawhub.ai/user/1u1s4)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operators with authenticated Gmail access use this skill to standardize sender-to-label routing, apply labels to existing messages, and optionally remove matching mail from the Inbox. It is useful when a user asks an agent to route one or more senders to a Gmail label using a repeatable workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can use stored Gmail credentials to create filters and apply label changes to existing messages.

Mitigation: Install only for accounts where this level of Gmail access is acceptable, and run with --dry-run before making changes.

Risk: Matching messages may be bulk moved out of the Inbox during retroactive application.

Mitigation: Verify sender addresses and label names carefully, and use --keep-inbox or --no-retro when inbox state should not change.

Risk: Using --replace-sender-filters can delete existing Gmail filters for the same sender.

Mitigation: Use --replace-sender-filters only when replacing existing sender filters is intentional.

## Reference(s):

- [Command Examples](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/1u1s4/skills/gmail-label-routing)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON]

**Output Format:** [Markdown guidance with bash command examples and JSON result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run, keep-inbox, no-retro, and replace-sender-filters options depending on the requested Gmail routing change.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
