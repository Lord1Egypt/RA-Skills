## Description:

一次调用完成搜索与推荐，含预订链接和退改政策解读，自动识别商务/亲子/度假/背包场景智能推荐，3档价格分选，零配置即装即用。暑假出境游全球住宿推荐，覆盖200+国家

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search global hotel options, classify trip scenarios, compare price tiers, and explain booking and cancellation details in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel-search details, including destination, dates, query text, budget preferences, and possible family or occupancy information, are sent through the skill's cloud proxy.

Mitigation: Install and use the skill only when this data flow is acceptable for the intended users and travel-planning workflow.

Risk: Hotel prices, availability, booking links, and cancellation terms can be time-sensitive or differ from the final booking page.

Mitigation: Confirm live prices, availability, and cancellation terms on the linked booking page before making travel decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/global-hotel-search-recommend)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style recommendation text with hotel names, prices, booking links, rationale, and cancellation-policy summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live hotel data returned through the disclosed cloud proxy; prices and availability can change.]

## Skill Version(s):

1.6.19 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
