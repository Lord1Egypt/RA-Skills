## Description:

Public Telegram data through okdata: channels, messages. 3 endpoints, $0.002 a call. Use when a task needs Telegram data. 通过 okdata 取Telegram公开数据：channels、messages。3 个接口，每次 $0.002。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and agents use this skill to look up public Telegram channel profiles, recent channel messages, and individual message details through okdata. It provides data without requiring a Telegram account, cookie, or QR login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill involves a named external service and may require its API key.

Mitigation: Review the service and call pricing before use; keep OKDATA_API_KEY in secure environment or client configuration and do not expose it.

Risk: The security scan had partial coverage because some local path-like references could not be resolved.

Mitigation: Review the skill and unresolved references before installation; treat the benign scan verdict as limited evidence, not a guarantee.

## Reference(s):

- [okdata Telegram API contract](https://okdata.online/apis/telegram/?src=skill-okdata-telegram)
- [okdata agent setup instructions](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [Text results for Telegram channel and message data, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; channel message listings return about 20 posts per page. Each data call costs $0.002.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
