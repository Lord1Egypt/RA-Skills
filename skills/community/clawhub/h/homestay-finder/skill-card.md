## Description: <br>
特色民宿搜索与AI智能推荐，覆盖景区民宿、古镇客栈、乡村精品民宿，多旅游平台数据直连，零配置即装即用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users use this skill to search and compare distinctive homestays, inns, and boutique stays by destination, dates, points of interest, price, and natural-language preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Homestay destinations, dates, nearby points of interest, budget, and preference text are sent to the skill's cloud proxy and travel providers. <br>
Mitigation: Avoid using the skill for sensitive travel plans and review privacy requirements before deployment. <br>
Risk: Any PROXY_TOKEN environment variable in the runtime is sent to the proxy endpoints. <br>
Mitigation: Use a scoped proxy token only when needed and avoid placing unrelated secrets in the runtime environment. <br>
Risk: Travel prices and availability can change after results are returned. <br>
Mitigation: Confirm price, availability, and booking terms on the linked provider page before purchasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/homestay-finder) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted travel recommendations with prices, ratings, addresses, images, source labels, and booking links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are generated from external travel proxy responses and may change with provider availability and pricing.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence; artifact frontmatter reports 1.2.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
