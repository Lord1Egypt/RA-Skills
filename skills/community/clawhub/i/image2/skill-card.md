## Description: <br>
image2 helps an agent create and poll text-to-image or reference-image generation tasks through the kexiangai.com image2 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runninghcm](https://clawhub.ai/user/runninghcm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to submit image-generation prompts, optionally include reference image URLs, and retrieve final generated image URLs after asynchronous polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, and task metadata are sent to kexiangai.com for processing. <br>
Mitigation: Use the skill only when the user accepts third-party processing by kexiangai.com and avoids submitting sensitive prompts or reference URLs. <br>
Risk: The optional local key helper stores X_API_KEY in a plaintext file at ~/.config/image2/.env. <br>
Mitigation: Prefer a session-scoped X_API_KEY environment variable; if local storage is used, keep file permissions restricted and rotate or remove the key when it is no longer needed. <br>
Risk: Creating or retrying image tasks may consume provider credits. <br>
Mitigation: Confirm task parameters before creation, create only one task per user request, and require explicit user approval before any retry. <br>


## Reference(s): <br>
- [image2 API Guide](references/api-guide.md) <br>
- [ClawHub image2 skill page](https://clawhub.ai/runninghcm/image2) <br>
- [Create image task endpoint](https://kexiangai.com/api/v1/user_task/asyncCreateWithCost) <br>
- [Query image task endpoint](https://kexiangai.com/api/v1/user_task/get/passAuth/{id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell commands and API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated task IDs, task status, final image URLs, and masked credential previews.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
