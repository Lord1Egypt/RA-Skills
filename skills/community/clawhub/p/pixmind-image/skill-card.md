## Description:

Generate or edit AI images with Pixmind for text-to-image, image-to-image, image editing, product images, posters, covers, and consistent characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuyunzhishang](https://clawhub.ai/user/fuyunzhishang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent route Pixmind image generation and editing requests, preserve visual constraints, submit approved jobs, poll task status, and return generated image attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pixmind prompts, reference-image URLs, and the PIXMIND_API_KEY may be used with the documented aihub-admin.aimix.pro endpoint.

Mitigation: Install only if that data sharing is acceptable, prefer the native Pixmind Builder tools, and avoid sensitive prompts or signed private image URLs.

Risk: Fallback scripts can print prompts, task results, image URLs, or errors into terminal and agent logs.

Mitigation: Use the native Builder tools when available and review logs for sensitive content if fallback scripts are used.

Risk: A failed or ambiguous paid image generation task could lead to duplicate submissions if retried carelessly.

Mitigation: Check the existing task status first and obtain fresh user approval before submitting another paid generation request.

## Reference(s):

- [Pixmind image model routing](references/model-routing.md)
- [Pixmind skill page](https://clawhub.ai/fuyunzhishang/skills/pixmind-image)
- [Pixmind API key dashboard](https://www.pixmind.io/api-platform/dashboard/keys)
- [Pixmind API platform endpoint](https://aihub-admin.aimix.pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance]

**Output Format:** [Markdown summaries with structured tool or API responses and generated image attachments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model, task ID, output count, image URLs, and terminal output when fallback scripts are used.]

## Skill Version(s):

2.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
