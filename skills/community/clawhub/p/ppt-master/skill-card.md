## Description: <br>
PPT Master helps agents turn documents and web content into presentation decks, SVG visuals, social graphics, posters, and PPTX exports through a multi-role workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzfxxx](https://clawhub.ai/user/lzfxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and business users use this skill to convert source PDFs, Markdown, and web pages into structured presentation or visual-content projects with planning, SVG generation, post-processing, and PPTX export guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes and recommends a Gemini watermark-removal tool, which may create asset-rights or policy concerns. <br>
Mitigation: Remove or avoid the watermark-removal workflow and confirm that generated or downloaded images are licensed for the intended presentation use. <br>
Risk: Web-to-Markdown conversion can fetch arbitrary URLs and the security summary notes weak transport safeguards. <br>
Mitigation: Run URL conversion only on public or authorized pages, review network behavior before use, and apply appropriate TLS and network safeguards. <br>
Risk: Presentation workflows may send confidential project content to third-party image-generation services. <br>
Mitigation: Do not submit confidential or regulated content to external services without approval; use approved internal tools or sanitized prompts when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lzfxxx/ppt-master) <br>
- [README_EN.md](README_EN.md) <br>
- [Tools usage guide](tools/README.md) <br>
- [Role definitions](roles/README.md) <br>
- [Chart template library](templates/charts/README.md) <br>
- [Online examples preview](https://hugohe3.github.io/ppt-master/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated project files such as SVG pages and PPTX exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local project folders, converted Markdown, embedded image assets, finalized SVG files, speaker notes, and PowerPoint files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and README badge) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
