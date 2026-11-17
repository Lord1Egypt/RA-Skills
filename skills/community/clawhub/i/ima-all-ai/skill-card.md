## Description:

IMA Studio All-in-One helps agents create images, videos, music, and text-to-speech assets through the IMA Open API with runtime model discovery and optional workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate and coordinate AI media assets across image, video, music, and speech workflows. It is suited for creative production tasks such as product demos, social campaigns, character-consistent media, and multi-step content pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generation settings, and local input images may be sent to IMA/CDN services.

Mitigation: Use the skill only for media and prompts that are appropriate to share with those services, and avoid submitting sensitive source material.

Risk: Authenticated API traffic can be redirected if a custom base URL is used.

Mitigation: Keep the default service endpoint, avoid custom --base-url values, and use a scoped or test IMA_API_KEY where possible.

Risk: Operational logs may retain sensitive prompt, request, or media URL details.

Mitigation: Periodically review and delete ~/.openclaw/logs/ima_skills, especially after failed requests or sensitive experiments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/skills/ima-all-ai)
- [IMA Studio](https://imastudio.com/)
- [IMA API key management](https://www.imaclaw.ai/imaclaw/apikey)
- [IMA subscription and credits](https://www.imaclaw.ai/imaclaw/subscription)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON result payloads containing generated media URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_API_KEY; generated media output is returned primarily as service-hosted URLs.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
