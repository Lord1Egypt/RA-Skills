## Description: <br>
孔夫子旧书网拍卖栏目检索技能，自动搜索安康、来鹿堂、兴安府三个关键词相关文献拍品。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobemsk](https://clawhub.ai/user/tobemsk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and collectors use this skill to search Kongfz auction listings for Ankang-related books, documents, and local-history materials. It guides browser-based searches, extracts listing text, and classifies matches by relevance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a local browser through xbrowser and opens Kongfz search pages, which may use the browser profile's existing cookies. <br>
Mitigation: Run it with a separate or logged-out browser profile when existing Kongfz session data should not be used. <br>
Risk: The provided script accepts one keyword per run even though the release advertises three fixed keywords. <br>
Mitigation: Run or orchestrate separate searches for 安康, 来鹿堂, and 兴安府, then compare the grouped results. <br>
Risk: Kongfz page structure and element references can change, causing stale browser automation selectors. <br>
Mitigation: Refresh the xbrowser snapshot before filling fields and update the element reference when the page structure changes. <br>


## Reference(s): <br>
- [Kongfz site structure reference](references/kongfz_structure.md) <br>
- [Kongfz actual structure update](references/kongfz_actual_structure.md) <br>
- [Kongfz auction advanced search](https://search.kongfz.com/adv.html?type=pm) <br>
- [Kongfz auction search result format](https://search.kongfz.com/pm-search-web/pc/auction/search?key=关键词) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style search summaries with inline shell command examples and prioritized listing details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are grouped by keyword and relevance priority when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
