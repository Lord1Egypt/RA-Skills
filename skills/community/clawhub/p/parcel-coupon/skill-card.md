## Description: <br>
Fetches parcel and courier coupon offers through a third-party API and returns coupon links and QR code image URLs for redemption through WeChat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moooai](https://clawhub.ai/user/moooai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current parcel shipping coupon information for services such as 顺丰, 中通, 圆通, 韵达, 申通, 菜鸟, and local delivery. The skill presents the returned title, coupon link, QR code image URL, and usage guidance without modifying returned coupon URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled documentation mismatch may cause an agent to explain or use a takeout coupon service instead of the parcel coupon service. <br>
Mitigation: Review and correct mismatched reference documentation before deployment; use the parcel coupon behavior in SKILL.md and scripts/fetch_coupons.py as the intended behavior. <br>
Risk: Returned coupon links and QR code image URLs are third-party content. <br>
Mitigation: Inspect destination domains where possible, present links as third-party content, and avoid modifying the URLs returned by the API. <br>
Risk: The external coupon API may fail, time out, or return an unexpected response structure. <br>
Mitigation: Handle network and parsing errors gracefully, and verify expected fields before presenting coupon links or QR code image URLs to users. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/moooai/parcel-coupon) <br>
- [Homepage from ClawHub metadata](https://github.com/moooai/parcel-coupon) <br>
- [Parcel coupon API endpoint](https://agskills.moontai.top/coupon/parcel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON containing coupon titles, third-party coupon links, QR code image URLs, and redemption guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party URLs and QR code image URLs returned by the parcel coupon API.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
