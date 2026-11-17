## Description:

Single-gateway image generation CLI for async text-to-image and image-to-image, with polling, download handling, and request alignment to the current gateway OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn text prompts or reference images into generated images through a WeryAI gateway workflow. It supports model selection, prompt assembly, style presets, async polling, downloads, dry runs, and batch generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed or overused if persisted carelessly.

Mitigation: Use a dedicated, low-quota WeryAI API key and avoid persisting it unless necessary.

Risk: Local files, reference images, prompt files, or batch inputs can contain sensitive information that may be sent to the external gateway.

Mitigation: Use only approved, non-sensitive inputs and avoid passing sensitive local files through --ref or batch files.

Risk: Generated result URLs and webhook URLs are external network destinations.

Mitigation: Review URLs before sharing them or using webhooks, and treat returned image links as externally hosted assets.

Risk: Runtime setup through npx -y bun can fetch executable tooling at install or run time.

Mitigation: Prefer a preinstalled and pinned Bun runtime before using the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/632657122/skills/image-generation-2)
- [Gateway Alignment Notes](references/weryai-platform.md)
- [First-Time Setup](references/config/first-time-setup.md)
- [Model Registry Schema](references/config/model-registry-schema.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Style Presets](references/style-presets.md)
- [WeryAI API Introduction](https://docs.weryai.com/en)
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task)
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task)
- [WeryAI Task Status API](https://docs.weryai.com/api-reference/tasks/query-task-details)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Generated image files or URLs, with JSON summaries for dry-run and batch modes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous task polling, optional batch concurrency, local model preferences, and optional local output downloads.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter version: 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
