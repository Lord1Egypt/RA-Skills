## Description: <br>
Detects graphic trademarks in product images and searches for visually similar registered marks to help assess logo-related trademark risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce sellers, brand owners, and agents use this skill to compare product images against graphic trademark records across supported regions before publishing or reviewing listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product images, titles, suspected logo names, and API-key-authenticated requests to LinkFox services for analysis. <br>
Mitigation: Install and use it only where LinkFox is an approved processor for the product data and credentials involved. <br>
Risk: The skill asks agents to send feedback about interactions to a separate LinkFox endpoint. <br>
Mitigation: Review or disable automatic feedback behavior before use in confidential business workflows. <br>
Risk: Trademark similarity results can inform risk screening but are not legal advice. <br>
Mitigation: Use the results as a review signal and route high-similarity or business-critical cases to qualified trademark review. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/linkfox-ai/linkfox-ruiguan-graphic-trademark) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, markdown] <br>
**Output Format:** [Markdown guidance with JSON request examples and tabular result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an image URL or base64 image data and a LinkFox API key; detection result count is capped at 100 per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
