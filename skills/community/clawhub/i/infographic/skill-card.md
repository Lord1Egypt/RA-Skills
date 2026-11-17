## Description:

Generate high-density infographics with structured layout and style choices and bundled generation tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn source material into a dense single-page infographic by organizing the content, selecting a layout and style, and generating image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference image handling may upload local files even though the documentation says local paths are rejected.

Mitigation: Use HTTPS public URLs for reference images and avoid passing local files with `--ref` until the implementation behavior matches the documentation.

Risk: API-key persistence can expose credentials if local configuration files are not protected.

Mitigation: Prefer an environment variable or protected secret store; if a key is persisted, restrict file permissions and review the project configuration.

Risk: The workflow depends on network calls to WeryAI and local JavaScript runtimes.

Mitigation: Review before installing, use a trusted preinstalled or pinned Bun runtime, and run only with content that may be sent to WeryAI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/632657122/skills/infographic)
- [Analysis Framework](references/analysis-framework.md)
- [Structured Content Template](references/structured-content-template.md)
- [Infographic Layouts and Styles](references/layouts-and-styles.md)
- [Prompt Template](references/prompt-template.md)
- [WeryAI text-to-image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task)
- [WeryAI image-to-image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Images, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated working files, JSON batch configuration, and image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces infographic image files and optional compressed WebP outputs; may also create analysis, structured-content, prompt, batch, and local configuration files.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
