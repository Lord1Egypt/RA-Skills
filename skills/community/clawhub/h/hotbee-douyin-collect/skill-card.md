## Description:

Parses Chinese-language Douyin data requests and calls HotBee APIs for public video, comment, creator, fan portrait, and hashtag data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanye1402-hash](https://clawhub.ai/user/shanye1402-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Chinese natural-language Douyin collection requests and explicit public Douyin links or identifiers into HotBee API calls and result summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run unaudited remote GitHub code that may receive a local HotBee API key.

Mitigation: Review before installing, run in a restricted environment, expose only HOTBEE_API_KEY, and rotate the key if it may have been logged or sent somewhere unintended.

Risk: Some public Douyin catalog routes are stale and may fail or return misleading availability signals.

Mitigation: Use only confirmed routes from references/api.md unless HotBee publishes an updated contract or a fresh probe confirms restoration.

Risk: Key-authenticated calls may consume HotBee quota.

Mitigation: Confirm user intent before live VIP endpoint calls unless the user already approved the spend.

## Reference(s):

- [Douyin API reference](references/api.md)
- [HotBee Skills](https://www.hotbee.cn/skills)
- [ClawHub skill page](https://clawhub.ai/shanye1402-hash/skills/hotbee-douyin-collect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run command examples, HotBee API route selection guidance, and redacted error details.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
