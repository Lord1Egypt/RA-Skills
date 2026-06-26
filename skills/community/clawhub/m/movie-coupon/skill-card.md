## Description: <br>
Fetches movie ticket coupon information for platforms such as Taopiaopiao and Maoyan, returning redemption links and QR code image URLs for users to redeem via WeChat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moooai](https://clawhub.ai/user/moooai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current movie ticket coupon offers, then present the coupon title, redemption link, QR code image URL, and usage guidance. It is intended for movie-ticket discount requests and follow-up questions about opening coupon links or scanning QR codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may be directed to external redemption links or QR code destinations. <br>
Mitigation: Check the destination before opening a coupon link or scanning a QR code, especially when a broad movie-related request triggers coupon output. <br>
Risk: The skill depends on a live coupon API, so returned offers, URLs, or availability can change. <br>
Mitigation: Present coupon data as returned by the API and give a retry or fallback message when the API is unavailable or returns unexpected data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moooai/movie-coupon) <br>
- [Publisher profile](https://clawhub.ai/user/moooai) <br>
- [Project homepage from metadata](https://github.com/moooai/movie-coupon) <br>
- [API documentation](references/api_documentation.md) <br>
- [Movie coupon API endpoint](https://agskills.moontai.top/coupon/movie) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with coupon title, redemption URL, QR code image URL, and usage guidance; helper script output may be formatted text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to the coupon API and presents external redemption URLs and QR code image URLs exactly as returned.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
