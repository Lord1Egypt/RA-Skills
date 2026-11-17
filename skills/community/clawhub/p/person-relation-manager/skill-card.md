## Description:

人物关系与平台昵称管理器。当需要给某人发消息、但不知道对方在某平台的昵称时触发。自动查询记忆，如果没有记录则询问用户并记忆。

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvin-dean](https://clawhub.ai/user/calvin-dean)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to look up a person's platform-specific nickname or contact handle before sending a message. When no profile exists, it asks the user for contact details and stores a reusable person profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores persistent contact profiles that can include real names, gender, platform handles, relationships, occupations, interests, and notes.

Mitigation: Store only information the user has permission to keep, minimize sensitive fields, and prefer aliases or platform handles unless real names or gender are necessary.

Risk: Stored person profiles may be outdated, incomplete, or misattributed across platforms.

Mitigation: Confirm the target identity before using a recalled handle for messaging and update or delete stale details when discovered.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvin-dean/skills/person-relation-manager)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Markdown or plain text with structured contact-profile fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recalled platform handles, prompts for missing profile fields, and memory entries for future lookup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
