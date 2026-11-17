## Description:

Microsoft 365 spam folder manager for Outlook/Exchange mailboxes that analyzes junk messages, scores suspicious patterns, and helps agents review or clean up spam.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tradmangh](https://clawhub.ai/user/tradmangh)

### License/Terms of Use:


## Use Case:

Developers, administrators, and mailbox operators use this skill to inspect Microsoft 365 junk folders, score suspicious messages, and move or label messages during spam review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox-changing commands can alter Outlook or Exchange mailbox state without the confirmations described in the skill documentation.

Mitigation: Use trusted Microsoft profiles, prefer dry-run or manual review workflows, and require explicit operator approval before running move or labeling commands.

Risk: Spam scoring can misclassify legitimate mail as suspicious or confirmed spam.

Mitigation: Review scores and reasons before moving messages, especially for shared mailboxes or messages from business-critical senders.

## Reference(s):

- [M365 Spam Manager on ClawHub](https://clawhub.ai/tradmangh/skills/m365-spam-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Microsoft 365 profile names, mailbox addresses, message identifiers, spam scores, categories, and folder actions.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
