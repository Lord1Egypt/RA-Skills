## Description:

Memo Collect helps agents record, list, and delete short local memo notes for a user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondli](https://clawhub.ai/user/bondli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Memo Collect to add, review, and remove short reminders or notes through a Node.js command-line skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memos are stored in a local JSON file under the user's home directory and may contain sensitive user notes.

Mitigation: Avoid storing secrets or regulated data unless the local environment's file protections are appropriate.

Risk: delete_memo permanently removes memo entries, and completion-style requests may be interpreted as deletion requests.

Mitigation: Confirm the memo number and deletion intent before invoking delete_memo.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Text, Files]

**Output Format:** [Plain text command output with a local JSON memo data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memo data in a JSON file under the user's home directory; delete_memo permanently removes selected entries.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
