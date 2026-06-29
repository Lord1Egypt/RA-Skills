## Description: <br>
搜索万豪集团旗下酒店并返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索，多旅游平台数据直连。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search Marriott-family hotels, inspect hotel details, and obtain package or booking links for a destination or specific property. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search terms, dates, hotel names, and the configured proxy token are sent to the proxy service used for live travel data. <br>
Mitigation: Use only a trusted PROXY_URL and scope PROXY_TOKEN only for this proxy. <br>
Risk: Hotel prices and availability are live travel data and may change before booking. <br>
Mitigation: Show the returned booking link and have the user confirm the final price and terms on the booking page. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown text with hotel results, details, prices, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns live proxy-backed travel data; default result lists are limited by the tool.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
