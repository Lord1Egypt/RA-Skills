## Description:

卖家之家跨境电商物流海外仓搜索

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search MJZJ cross-border e-commerce logistics provider labels and logistics providers, including overseas warehouses, dedicated lines, customs clearance, and related services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support authenticated outbound provider messaging through a related endpoint when MJZJ_API_KEY is configured.

Mitigation: Configure MJZJ_API_KEY only for agents trusted to initiate provider contact, and require explicit user confirmation of the recipient and message content before sending a private message.

Risk: Snowflake-style IDs can lose precision if an agent or client treats them as numbers.

Mitigation: Handle id, labelIds, and nextPosition values strictly as strings throughout lookup and follow-up workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-wuliu)
- [MJZJ homepage](https://mjzj.com)
- [MJZJ logistics labels endpoint](https://data.mjzj.com/api/spQuery/getLogisticsLabels)
- [MJZJ logistics providers endpoint](https://data.mjzj.com/api/spQuery/queryLogisticsProviders)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference the MJZJ_API_KEY environment variable when explaining authenticated follow-up messaging.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
