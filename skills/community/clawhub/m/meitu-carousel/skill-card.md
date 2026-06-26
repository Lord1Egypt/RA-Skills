## Description: <br>
Generates a coordinated carousel set with a cover poster and matching inner pages for social posts, knowledge cards, and product introductions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meitu](https://clawhub.ai/user/meitu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and operators use this skill to turn a topic or supplied copy into a consistent multi-image carousel, including cover copy, page copy, image-generation prompts, refinement guidance, and saved poster files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, draft copy, and reference images may be processed by Meitu during image generation. <br>
Mitigation: Use the skill only with content approved for Meitu processing, and avoid confidential images or proprietary campaign text unless that sharing is authorized. <br>
Risk: Project mode can read and persist style preferences across visual workspace memory files. <br>
Mitigation: Review the configured visual workspace before use, inspect or delete stored memory files when needed, and use one-off mode when preferences should not be retained. <br>
Risk: The skill depends on Meitu CLI credentials and writes generated image files to local output paths. <br>
Mitigation: Keep Meitu API credentials scoped and protected, verify the resolved output directory before generation, and review generated files before publishing. <br>


## Reference(s): <br>
- [Meitu Carousel on ClawHub](https://clawhub.ai/meitu/meitu-carousel) <br>
- [Xiaohongshu cover reference](references/xiaohongshu-cover.md) <br>
- [Memory protocol](references/memory-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JPEG poster files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Meitu CLI credentials and can save cover and inner-page images to a project or visual workspace output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
