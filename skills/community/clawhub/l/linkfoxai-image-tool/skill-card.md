## Description: <br>
linkfoxai-image-tool helps agents upload images, create scene variants, replace products, remove image backgrounds, and retrieve image-generation task results through Linkfox/ZNOPEN image tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziniao-open](https://clawhub.ai/user/ziniao-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run supported Linkfox image workflows directly, including image upload, scene fission, product replacement, automatic image matting, and result lookup. It is intended for requests where the user wants the final processed image result rather than integration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store a provider API key locally for Linkfox/ZNOPEN API access. <br>
Mitigation: Use a scoped API key, confirm before allowing the agent to save credentials, and rotate or revoke the key when it is no longer needed. <br>
Risk: Selected images may be uploaded to the provider for processing. <br>
Mitigation: Send only images that are appropriate for external provider processing and avoid submitting sensitive or restricted content unless policy allows it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziniao-open/linkfoxai-image-tool) <br>
- [Linkfox OpenAPI router](https://sbappstoreapi.ziniao.com/openapi-router) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Text or JSON responses with image URLs, task identifiers, status values, and error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a ZNOPEN_API_KEY or local ~/.znopen/config.json when calling the provider API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
