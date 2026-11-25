## Description:

Access public WeChat Channels videos, accounts, comment replies, collections, and backup data through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to find public WeChat Channels content and inspect accounts, comments, collections, live replays, and engagement metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rated the skill benign with medium confidence and partial coverage; it does not establish the safety of the referenced external API or unmatched references.

Mitigation: Review the okdata service and references before use, and proceed only if you trust the service.

Risk: API calls can incur charges, and additional pages require additional paid calls.

Mitigation: Check the endpoint price and set an appropriate max_price before each paid call; request more pages only when needed.

## Reference(s):

- [WeChat Channels API reference](https://okdata.online/apis/wechat_channels/?src=skill-okdata-wechat-channels)
- [okdata agent setup instructions](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [text, guidance, API data]

**Output Format:** [Markdown instructions and text results returned by the okdata API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per API call; requesting more pages requires additional paid calls.]

## Skill Version(s):

0.2.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
