## Description:

Generate AI video via Infinimo AI Design using first/last frame, free-form asset, or prompt-only modes, with support for model lookup, credit estimates, uploads, job submission, and result polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators use this skill to generate e-commerce-oriented videos through the Infinimo AI Design API from prompts, uploaded media assets, or first and last frame inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded media, and API credentials are sent to the Clawec/Infinimo cloud API.

Mitigation: Use an approved Infinimo token and avoid uploading confidential, regulated, or proprietary prompts or media unless the service is approved for that data.

Risk: The documented log deletion endpoint can remove video generation records.

Mitigation: Confirm the target job and retention requirements before using any deletion action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/infinimo-ai-design-video-create)
- [Publisher Profile](https://clawhub.ai/user/anyunzhong)
- [Infinimo AI Design](https://design.infinimo.ai/?source=q-i-d-clawhub)
- [Infinimo API Key](https://design.infinimo.ai/api-key?source=q-i-d-clawhub)
- [Video Generation Response Schema](references/response-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated video URLs, submitted job parameters, model-option lookups, credit estimates, and polling summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
