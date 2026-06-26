## Description: <br>
Generate ad creatives, marketing images, and advertising visuals using the Promify API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[promify](https://clawhub.ai/user/promify) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketers, developers, and agents use this skill to extract product-page details and request generated ad creatives, marketing images, creative copy, and remaining quota from Promify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires storing and using a Promify API key. <br>
Mitigation: Store the key only in the OpenClaw configuration entry for this skill and rotate or remove it when access is no longer needed. <br>
Risk: Product details and image URLs from fetched pages are sent to Promify for creative generation. <br>
Mitigation: Avoid private, internal, pre-release, or confidential product pages unless the user has approved sending those details to Promify. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/promify/promify-creative-generator) <br>
- [Promify](https://promify.ai) <br>
- [Promify image task API endpoint](https://promify.ai/open-api/image/tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with product summaries, API results, image URLs, creative copy, quota status, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PROMIFY_API_KEY from OpenClaw configuration, submits extracted product details to Promify, and polls for up to 3 minutes.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
