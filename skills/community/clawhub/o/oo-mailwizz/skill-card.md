## Description:

MailWizz (mailwizz.com). Use this skill for ANY MailWizz request — reading, creating, updating, and deleting data. Whenever a task involves MailWizz, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing teams use this skill to inspect MailWizz mailing lists and subscribers, and to create, update, or unsubscribe subscribers through their connected account. Subscriber changes require approval under the skill's operating guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path runs a remote CLI installer whose behavior is unverified, and the CLI has a documented startup skill synchronization step.

Mitigation: Review and verify the installer before setup; consider setting OO_SKILLS_SYNC_DISABLED=1 before CLI use.

Risk: Connector requests are made through OOMOL using the connected MailWizz account.

Mitigation: Connect only the intended account and understand that OOMOL processes connector requests.

Risk: Subscriber creation or updates change account data, and unsubscribe is destructive.

Mitigation: Keep approval for subscriber changes and obtain explicit approval before an unsubscribe action.

## Reference(s):

- [MailWizz skill release](https://clawhub.ai/oomol/skills/oo-mailwizz)
- [MailWizz](https://www.mailwizz.com)
- [MailWizz API documentation](https://api-docs.mailwizz.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON connector requests and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific requests follow the live connector schema.]

## Skill Version(s):

1.0.4 (source: frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
