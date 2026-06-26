## Description: <br>
Generate images via Krea.ai API - Nano Banana 2 (default), Flux, Imagen 4, Seedream 3, Ideogram 3.0, Nano Pro/base, and return direct URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomas-mikula](https://clawhub.ai/user/tomas-mikula) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to submit explicit image-generation requests to Krea.ai, select supported image models, and receive generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Krea API token and sends prompts or referenced image URLs to Krea. <br>
Mitigation: Use a revocable token and avoid confidential prompts or private image URLs unless that fits the user's data policy. <br>
Risk: Frequent job submission or polling can trigger Krea API rate limits. <br>
Mitigation: Submit at most one job every 10 seconds, poll every 5-8 seconds, and back off before retrying after 429 responses. <br>


## Reference(s): <br>
- [Krea API Developer Documentation](https://docs.krea.ai/developers/introduction) <br>
- [Krea API Token Settings](https://krea.ai/settings/api-tokens) <br>
- [ClawHub Skill Page](https://clawhub.ai/tomas-mikula/krea-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown list of generated image URLs with a short model summary or error guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KREA_API_TOKEN and sends prompts or referenced image URLs to Krea.ai.] <br>

## Skill Version(s): <br>
1.0.2 (source: skill frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
