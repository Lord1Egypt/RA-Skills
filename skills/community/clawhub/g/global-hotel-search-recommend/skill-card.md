## Description: <br>
一次调用完成搜索与推荐，含预订链接和退改政策解读，自动识别商务/亲子/度假/背包场景智能推荐，3档价格分选，零配置即装即用。暑假出境游全球住宿推荐，覆盖200+国家 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search hotels globally, compare recommendations across business, family, vacation, backpacking, and general travel scenarios, and present booking links with plain-language cancellation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search text, destination, dates, occupancy, budget, and preferences may be shared with an external proxy and downstream hotel service. <br>
Mitigation: Install only when that data sharing is acceptable, avoid entering sensitive personal details, and require clear network and data-sharing disclosure before broad use. <br>
Risk: The artifact behavior and security summary indicate an embedded proxy token. <br>
Mitigation: Remove or rotate the embedded token and use publisher-managed or user-scoped credentials before treating the skill as broadly deployable. <br>
Risk: The security guidance flags weak permission disclosure for the external hotel proxy. <br>
Mitigation: Review the activation scope and endpoint behavior before deployment, and keep the skill in review status until disclosure is narrowed and documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/global-hotel-search-recommend) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style Chinese hotel recommendation text with hotel lists, prices, image links, booking links, and cancellation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include real-time prices, fallback search warnings, and proxy-sourced hotel data notices.] <br>

## Skill Version(s): <br>
1.6.3 (source: server release evidence; artifact frontmatter reports 1.6.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
