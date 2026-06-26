## Description: <br>
Convert photos and images into cartoon-style illustrations using AI via Media.io OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check Media.io credits, submit reachable image URLs for cartoon conversion, poll asynchronous task status, and return generated preview URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs are sent to Media.io for third-party processing. <br>
Mitigation: Use only user-authorized images and avoid sensitive or private photos unless Media.io's terms and data handling meet the deployment requirements. <br>
Risk: The skill requires a Media.io API key and may consume account credits. <br>
Mitigation: Keep MEDIAIO_API_KEY out of logs and responses, check available credits before generation, and monitor account usage. <br>
Risk: Generated cartoon images are synthetic edited media that could be mistaken for original photos. <br>
Mitigation: Present generated outputs as edited synthetic content and do not imply identity verification or biometric certainty. <br>


## Reference(s): <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY and a Media.io-reachable image URL; successful calls return generated image preview URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
