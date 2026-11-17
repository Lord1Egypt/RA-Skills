## Description:

5项酒店搜索工具覆盖万豪品牌查询、酒店详情、套餐推荐、周边餐饮，基于途牛与高德数据直连，零配置即装即用。暑期酒店预订智能筛选，快速匹配理想住所

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask for domestic hotel options, booking links, and nearby food recommendations using natural-language travel queries. The active behavior sends hotel, restaurant, and location-related search text through disclosed cloud proxy services backed by Tuniu and Gaode data.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Hotel, restaurant, and location-related search text is sent to external cloud proxy services.

Mitigation: Install only when that data flow is acceptable for the intended users and avoid submitting sensitive personal or business travel details.

Risk: Marriott-specific search, detail, and package capabilities are advertised in the artifact documentation but currently return unavailable/service-adjusted messages.

Mitigation: Treat Marriott-specific claims as unavailable for this release and direct users to the active domestic hotel search or other hotel recommendation tools.

Risk: Hotel prices, ratings, availability, and booking links can change after the skill returns results.

Mitigation: Confirm final price, terms, and availability on the booking page before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/hotel-smart-pro)
- [Publisher profile](https://clawhub.ai/user/travel-skills)
- [Tuniu cloud proxy](https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com)
- [Gaode cloud proxy](https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown-like plain text with hotel, food, price, rating, address, data-source, booking-link, and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are query dependent, use external proxy APIs, and prices or availability can change before booking.]

## Skill Version(s):

1.1.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
