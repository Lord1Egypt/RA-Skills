## Description: <br>
Generate high-density infographics with structured layout and style choices and bundled generation tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn complex source material into a single high-density infographic with explicit content structure, layout choice, style direction, prompt files, batch configuration, and generated image output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Infographic prompts and referenced images are sent to WeryAI during generation. <br>
Mitigation: Install and run the skill only when that external processing is acceptable for the project data. <br>
Risk: The IMAGE_GEN_API_KEY can be persisted to local .env configuration when setup is run with persistence enabled. <br>
Mitigation: Prefer environment variables or a secret store, and confirm .image-skills files are gitignored before sharing or committing a project. <br>
Risk: Referenced images may expose source material to the image generation service. <br>
Mitigation: Use only intended public HTTPS reference URLs and avoid sensitive local or private image inputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/632657122/infographic) <br>
- [Analysis Framework](references/analysis-framework.md) <br>
- [Structured Content Template](references/structured-content-template.md) <br>
- [Infographic Layouts and Styles](references/layouts-and-styles.md) <br>
- [Prompt Template](references/prompt-template.md) <br>
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task) <br>
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task) <br>
- [WeryAI Platform](scripts/vendor/shared-image-generation/references/weryai-platform.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions, generated prompt files, JSON batch configuration, shell commands, and image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates analysis.md, structured-content.md, prompt markdown, optional batch.json, infographic image output, and compressed webp delivery files.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
