## Description:

한국형 쇼핑 검색 스킬. 네이버 쇼핑 API + 쿠팡/11번가 웹 스크래핑으로 배송비 포함 최저가를 자동 비교합니다.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT

## Use Case:

External users and shopping agents use this skill to search Korean shopping platforms and compare product prices with estimated shipping costs across Naver Shopping, Coupang, and 11st.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network and API requests may be logged or rate-limited by Naver, Coupang, and 11st.

Mitigation: Use dedicated Naver API credentials, run the skill in a virtual environment, and keep request volume within platform limits.

Risk: Scraped Coupang and 11st results can break or become inaccurate when site structures change.

Mitigation: Treat returned prices and shipping estimates as advisory and verify final purchase terms on the merchant product page.

Risk: Dependency installation with broad privileges can affect the host environment.

Mitigation: Install dependencies in an isolated virtual environment with pinned versions and avoid administrator-level pip installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/naver-shopping-plus)
- [Naver Developers](https://developers.naver.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text shopping results or structured JSON from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include product title, platform, price, estimated shipping, total price, and URL when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
