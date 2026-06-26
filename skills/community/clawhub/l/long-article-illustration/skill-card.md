## Description: <br>
Helps an agent segment long-form articles, generate illustration prompts, and optionally produce article images through a user-selected image-generation tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and agents use this skill to turn long blog, newsletter, and social publishing drafts into paragraph-level illustration plans, image prompts, and optional generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article text and generated prompts may be sent to the image-generation provider configured by the user. <br>
Mitigation: Use trusted providers, keep API keys outside the skill, and avoid sending confidential article content to providers that are not approved for that data. <br>
Risk: Generated images may raise copyright, likeness, or platform policy concerns. <br>
Mitigation: Review generated images before publication and regenerate or revise prompts when outputs appear unsafe, misleading, or rights-sensitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/antonia-sz/long-article-illustration) <br>
- [Style presets and prompt templates](references/style-presets.md) <br>
- [Paragraph segmentation rules](references/paragraph-rules.md) <br>
- [Troubleshooting guidance](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown article draft, prompt table, or image package guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include image-generation prompts and references to files produced by the user's chosen image tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
