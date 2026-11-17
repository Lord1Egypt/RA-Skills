## Description:

Generates images from text prompts or reference image URLs through the nano-banana2 imgEditNB2 API, with optional aspect ratio and image size settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runninghcm](https://clawhub.ai/user/runninghcm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images or image variations from prompts and optional reference-image URLs while selecting supported aspect ratios and resolution tiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference-image URLs, and the API key are sent to agent.mathmind.cn.

Mitigation: Install and use the skill only when that third-party data transfer is acceptable for the user's content and credentials.

Risk: A saved API key can be persisted locally and read when local-key mode is explicitly enabled.

Mitigation: Prefer the session-scoped X_API_KEY environment variable and use local-key mode only after choosing to accept local credential storage.

Risk: The documented stdin pipeline can expose real keys through command history or logs if copied directly.

Mitigation: Use interactive key entry or a session environment variable for real credentials.

## Reference(s):

- [nano-banana2 API Guide](references/api-guide.md)
- [ClawHub skill page](https://clawhub.ai/runninghcm/skills/nano-banana2)
- [imgEditNB2 API endpoint](https://agent.mathmind.cn/minimalist/api/imgEditNB2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, parameter summaries, and generated image result status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an image URL or an error summary from the third-party API.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
