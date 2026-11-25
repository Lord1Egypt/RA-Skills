## Description:

Use Feishu to read, create, update, and delete workspace data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected Feishu account use the skill to read and manage workspace data, including chats, messages, documents, calendars, mail, tasks, approvals, spreadsheets, and Bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs an unpinned installer fetched from the internet; its contents were not available for review, so its behavior is unknown.

Mitigation: Review the installer and verify its source and expected changes before running it; use a verified release when available.

Risk: Feishu write and destructive actions can change or remove workspace data.

Mitigation: Confirm the target and exact effect with the user before running any write or destructive action, as the skill directs.

## Reference(s):

- [Feishu developer documentation](https://open.feishu.cn/document/home/index)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Feishu homepage](https://www.feishu.cn)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured connector results, plus task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Feishu workspace data; some actions are destructive.]

## Skill Version(s):

1.0.9 (source: frontmatter; confirmed by server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
