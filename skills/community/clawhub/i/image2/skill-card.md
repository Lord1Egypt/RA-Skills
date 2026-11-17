## Description:

image2 creates and monitors asynchronous image-generation tasks through the kexiangai.com image2 API for text-to-image and reference-image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runninghcm](https://clawhub.ai/user/runninghcm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to validate prompts, aspect ratios, and optional reference image URLs, create one image-generation task, and poll until a final image URL or failure status is returned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The task script can send API keys and prompts to a caller-chosen API host.

Mitigation: Use the default kexiangai.com endpoint or only set IMAGE2_BASE_URL or --base-url to a trusted HTTPS endpoint intentionally chosen by the user.

Risk: API keys may be persisted locally when local-key mode is enabled.

Mitigation: Prefer a session-scoped X_API_KEY environment variable and use --use-local-key only when persistence is required.

Risk: The skill depends on an external image-generation provider.

Mitigation: Install and run it only if the user trusts kexiangai.com and has confirmed the provider is appropriate for the prompts and reference images being submitted.

## Reference(s):

- [image2 API Guide](references/api-guide.md)
- [ClawHub skill page](https://clawhub.ai/runninghcm/skills/image2)
- [Create image task endpoint](https://kexiangai.com/api/v1/user_task/asyncCreateWithCost)
- [Query image task endpoint](https://kexiangai.com/api/v1/user_task/get/passAuth/{id})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with shell command examples and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task IDs, task status, generated image URLs, failure reasons, and masked credential previews.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
