## Description: <br>
综合优惠券获取工具，支持外卖（美团、饿了么、京东）、快递（顺丰、中通、圆通等）、出行（滴滴、携程）、电影票（淘票票、猫眼）等全平台优惠券，一键获取所有优惠。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moooai](https://clawhub.ai/user/moooai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request coupon codes, coupon links, QR image URLs, and redemption guidance for takeout, parcel, travel, and movie-ticket platforms. It is suited for agents that need to collect and present currently available third-party coupon offers by category or platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill displays third-party coupon links and QR codes that may lead users outside the agent experience. <br>
Mitigation: Ask users to verify destinations before opening links or scanning QR codes, and avoid entering account, payment, or personal information unless they confirm the intended platform. <br>
Risk: Coupon APIs may be unavailable or returned offers may change, expire, or fail to redeem. <br>
Mitigation: Present API-returned coupon codes and links unchanged, include the returned redemption guidance, and provide retry or backup-skill guidance when an API call fails. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/moooai/obtain-coupons-all-in-one) <br>
- [Publisher Profile](https://clawhub.ai/user/moooai) <br>
- [Homepage](https://github.com/moooai/obtain-coupons-all-in-one) <br>
- [全平台优惠券API接口文档](references/api_documentation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with coupon codes, coupon URLs, QR image URLs, and redemption notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coupon codes, coupon URLs, and QR image URLs should be presented unchanged from the API response.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
