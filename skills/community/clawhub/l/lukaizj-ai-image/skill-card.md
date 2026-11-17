## Description:

AI image generation - Generate images using OpenAI DALL-E or other AI image APIs

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukaizj](https://clawhub.ai/user/lukaizj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate images from prompts, edit existing images, and create image variations through OpenAI image APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image edit and variation tools can upload any readable local file path supplied to the agent.

Mitigation: Run only in an environment where the agent cannot read sensitive files, restrict inputs to approved image files, and require explicit confirmation before file upload.

Risk: Generated prompts and selected image files are sent to OpenAI image endpoints.

Mitigation: Avoid submitting confidential prompts or files unless the deployment has approved that data flow and API usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukaizj/skills/lukaizj-ai-image)
- [Project homepage](https://github.com/lukaizj/ai-image-skill)

## Skill Output:

**Output Type(s):** [API Calls, Files, Code, Configuration instructions, Guidance]

**Output Format:** [JSON responses containing generated or edited image URLs, plus setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY and sends prompts or selected image files to OpenAI image endpoints.]

## Skill Version(s):

0.1.0 (source: server release evidence and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
