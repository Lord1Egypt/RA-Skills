## Description: <br>
Analyzes Amazon product listing titles to extract and count keyword patterns, scene words, audience terms, materials, and other attribute dimensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and e-commerce operators use this skill to analyze titles from already queried products, surface high-frequency title attributes, and compare competitor keyword patterns one attribute dimension at a time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product titles, product metadata, and related request context are sent to LinkFox services for analysis. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid submitting sensitive or restricted product data. <br>
Risk: The skill describes automatic feedback reporting to a separate LinkFox endpoint without clear user consent. <br>
Mitigation: Review feedback behavior before installation and require explicit opt-in or clear limits before sending feedback content. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Product Title Analyze on ClawHub](https://clawhub.ai/linkfox-ai/linkfox-product-title-analyze) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes one requested title-attribute dimension per API call; requires product data in the current conversation or refResultData.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
