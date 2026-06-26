## Description: <br>
闲鱼商品自动搜索技能，支持严格筛选（个人闲置/单一价格/排除商家），输出 TOP10 价格升序列表 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxxzhuo](https://clawhub.ai/user/xxxzhuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Xianyu/Goofish listings, filter for personal idle goods with single prices, sort candidate products by price, and return ranked results with links and price statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records detailed shopping searches and result links to persistent memory without clearly documented user consent, retention, or cleanup controls. <br>
Mitigation: Use it only when the user is comfortable saving that search history, avoid sensitive purchase searches, and provide a way to disable, review, or clear stored records before deployment. <br>
Risk: Browser-based marketplace results can include stale listings, misleading prices, or third-party seller content outside the skill publisher's control. <br>
Mitigation: Treat returned listings as candidates for manual review, verify seller details and item condition before purchase, and avoid sharing account credentials during browsing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xxxzhuo/gofilshsearcher) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xxxzhuo) <br>
- [Goofish website](https://www.goofish.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown search result tables and per-item chat messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ranked item titles, prices, regions, want counts, listing links, price statistics, and applied-filter notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
