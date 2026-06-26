## Description: <br>
Transforms knowledge content into a series of polished knowledge-card images, either by extracting points from articles or by using directly supplied knowledge points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hash-panda](https://clawhub.ai/user/hash-panda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, educators, and content teams use this skill to turn articles or structured notes into image-card series with selectable layouts, visual styles, platform presets, and optional character integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided source material, derived outlines, prompts, generated images, backups, and preferences may be saved under project or home-directory paths. <br>
Mitigation: Avoid sensitive or proprietary input unless local retention is acceptable, and review generated files before sharing or deploying them. <br>
Risk: Image generation is delegated to a separate image-generation skill or backend, which may have its own data-handling behavior and output limitations. <br>
Mitigation: Confirm the selected image-generation backend is acceptable for the content and review the generated images for accuracy, privacy, and brand suitability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hash-panda/panda-knowledge-card) <br>
- [Project homepage](https://github.com/hash-panda/panda-skills#panda-knowledge-card) <br>
- [Card layouts](artifact/references/card-layouts.md) <br>
- [Workflow](artifact/references/workflow.md) <br>
- [Prompt construction](artifact/references/prompt-construction.md) <br>
- [Styles](artifact/references/styles.md) <br>
- [Platform presets](artifact/references/platform-presets.md) <br>
- [Presets](artifact/references/presets.md) <br>
- [Preferences schema](artifact/references/config/preferences-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, outlines, prompt files, shell command snippets, and generated image-file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local outlines, prompt files, source backups when applicable, generated card images, and a completion report.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
