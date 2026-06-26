## Description: <br>
Turns product images and campaign copy into polished seasonal promo posters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuminliu026](https://clawhub.ai/user/shuminliu026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketing teams use this skill to turn product images, offers, and campaign copy into holiday-specific promotional posters through a guided agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a mew.design API key. <br>
Mitigation: Use a key that can be rotated or revoked, and stop using any key that returns an authentication error. <br>
Risk: Product images and campaign copy are sent to Mew's API to generate the poster. <br>
Mitigation: Use public URLs that the user controls and avoid sending confidential product assets unless the user accepts that data sharing. <br>
Risk: Local-only or attached images may need a temporary third-party upload before they can be used as API assets. <br>
Mitigation: Ask for explicit consent before uploading images to an external file host, and prefer user-provided public URLs when available. <br>


## Reference(s): <br>
- [Holiday Promo Poster ClawHub release](https://clawhub.ai/shuminliu026/holiday-promo-poster) <br>
- [Holiday Promo Poster Presets](references/holiday-presets.md) <br>
- [Mew design account and API key setup](https://mew.design/login) <br>
- [Mew design generation API endpoint](https://api.mew.design/open/api/design/generate) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown response with generated image links, plus JSON request bodies and shell commands during execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided mew.design API key and server-accessible product image URLs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
