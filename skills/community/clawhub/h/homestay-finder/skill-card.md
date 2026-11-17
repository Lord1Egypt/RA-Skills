## Description:

特色民宿搜索与AI智能推荐，覆盖景区民宿、古镇客栈、乡村精品民宿，多旅游平台数据直连，零配置即装即用。暑期避暑民宿推荐，古镇乡村特色住宿搜索

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to search Chinese homestays and inns by destination, keyword, attraction, dates, price, and sorting preference, then review prices, ratings, addresses, images, and booking links. The skill is also presented as offering natural-language homestay recommendations, but release security evidence says that recommendation behavior is currently unreliable.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Lodging search terms, destinations, and travel dates are sent through a disclosed cloud proxy.

Mitigation: Use the skill only when that routing is acceptable, avoid entering sensitive travel details, and review the disclosed data flow before deployment.

Risk: The release security summary says the AI recommendation command is broken and some recommendation or multi-platform comparison claims are unreliable.

Mitigation: Treat recommendation output and comparison claims as advisory, prefer structured search behavior, and verify lodging details and prices on the linked booking platform.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/homestay-finder)
- [Publisher profile](https://clawhub.ai/user/travel-skills)
- [Disclosed cloud proxy endpoint](https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted Chinese lodging search results with prices, ratings, addresses, optional images, booking links, source notes, and related travel prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped at up to 15 deduplicated listings and prices are real-time estimates that should be verified on the booking page.]

## Skill Version(s):

1.2.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
