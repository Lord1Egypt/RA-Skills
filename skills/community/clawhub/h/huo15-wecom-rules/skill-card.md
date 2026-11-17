## Description:

Provides standardized guidance for agents using WeCom APIs to send messages and files, including message formats, fallback handling, and user profile lookup behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Agents serving WeCom users can use this skill as operational guidance for sending direct messages, group notifications, card-style notices, news items, and files through WeCom. It is intended for messaging workflow standardization rather than standalone application logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports exposed WeCom credential and webhook material.

Mitigation: Review before installation, remove the exposed material, rotate affected credentials, and replace examples with placeholders or a secure integration layer.

Risk: The release evidence reports automatic cross-user storage of personal profile data in shared memory.

Mitigation: Require explicit user consent and scope profile data storage to the minimum necessary audience before enabling the behavior.

Risk: The skill directs agents to send WeCom messages and files, which can create unintended outbound communication.

Mitigation: Require explicit confirmation before sending messages or files, especially to groups or external recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-wecom-rules)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes WeCom message and file sending rules, fallback guidance, and user profile handling notes.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
