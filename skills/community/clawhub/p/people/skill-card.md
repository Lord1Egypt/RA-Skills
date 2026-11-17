## Description:

Maintains a personal address book for people the user mentions, including context, last contact, birthdays, anniversaries, introductions, and privacy boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to maintain a local contacts/address book, recall relationship context, prepare for meetings, track introductions, and draft person-specific messages without sending them automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores durable notes about third parties, including relationship context and life events.

Mitigation: Use it only when you want a local address book maintained by an agent, and review the local Clawic people and contacts files when privacy, sensitive details, or deletion behavior matters.

Risk: Contact files may contain sensitive relationship context if the user chooses to record it.

Mitigation: The skill documents a minimal sensitive-details default, suppression checks before surfacing people, and deletion behavior that removes records and regenerated exports when the user asks.

Risk: Credentials or access codes can appear in pasted contact notes or house-sitting context.

Mitigation: The skill instructs the agent to strip secret values before writing and store only pointers such as a vault, keychain, environment variable, or local credential file reference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/people)
- [Clawic Contacts skill page](https://clawic.com/skills/people)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown notes, contact rows, briefings, message drafts, and local configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates local Clawic contact files under the configured people and contacts paths; drafts messages but does not send them.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
