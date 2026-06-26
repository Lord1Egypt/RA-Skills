## Description: <br>
한국형 쇼핑 검색 스킬. 네이버 쇼핑 API + 쿠팡/11번가 웹 스크래핑으로 배송비 포함 최저가를 자동 비교합니다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search Korean shopping platforms, compare item prices including estimated shipping, and return ranked shopping results from Naver Shopping, Coupang, and 11st. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Naver, Coupang, and 11st. <br>
Mitigation: Use the skill only for searches that are acceptable to share with those services. <br>
Risk: The skill requires a Naver API client ID and secret. <br>
Mitigation: Store credentials in environment variables or a local .env file and avoid echoing secrets into shared logs or chats. <br>
Risk: Coupang and 11st scraping may break when page structure changes or may trigger blocking under heavy use. <br>
Mitigation: Keep request volume moderate, verify important results on the product page, and update selectors when platforms change their markup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mupengi-bot/naver-shopping-plus) <br>
- [Naver Developers](https://developers.naver.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Terminal-friendly text or JSON search results with product titles, prices, shipping estimates, platform labels, and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can be filtered by platform, maximum price, result count, and sort option.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
