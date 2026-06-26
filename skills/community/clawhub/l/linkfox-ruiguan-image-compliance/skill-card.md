## Description: <br>
Ruiguan Image Compliance screens product image URLs against a database of known policy-violating products using visual similarity matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External commerce operators and agents use this skill to pre-screen product image URLs for visual similarity to known policy-violating products before listing or review. It presents matches, similarity scores, and matched product images for human policy verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product image URLs are sent to the LinkFox/Ruiguan compliance service for analysis. <br>
Mitigation: Use the skill only when the user is comfortable sharing the image URL with LinkFox/Ruiguan and an authorized LINKFOXAGENT_API_KEY is configured. <br>
Risk: The artifact instructs the agent to report feedback and user-interaction context to a separate LinkFox feedback endpoint without interrupting the user's flow. <br>
Mitigation: Require confirmation before submitting feedback, or remove automatic feedback behavior when user comments, intent, or business context should not be reported externally. <br>
Risk: Similarity matches may be mistaken for definitive policy or legal rulings. <br>
Mitigation: Present scores and matched images factually, highlight high-similarity results for review, and direct users to verify decisions against applicable platform policies. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Listing](https://clawhub.ai/linkfox-ai/linkfox-ruiguan-image-compliance) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and factual guidance, with JSON responses from the helper script or API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a publicly accessible image URL up to 1000 characters and LINKFOXAGENT_API_KEY; results are similarity-based and should not be treated as legal conclusions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
