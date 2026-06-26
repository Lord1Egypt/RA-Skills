## Description: <br>
Generate and convert icons. Use when creating SVGs, building sprite sheets, converting ICO/PNG/SVG, or generating favicon sets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to generate SVG icons, assemble sprite sheets, convert icon formats, resize icon assets, and create favicon sets for web and app projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated and converted icon files to local output paths. <br>
Mitigation: Use project-local output directories and review input and output paths before running batch resize, conversion, or favicon commands. <br>
Risk: Raster and ICO conversion depends on local image conversion tools. <br>
Mitigation: Keep ImageMagick or librsvg up to date and process trusted image files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/icon) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands plus generated SVG, PNG, ICO, web manifest, and HTML snippet files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes icon outputs to user-specified local paths; PNG and ICO conversion may require ImageMagick or librsvg.] <br>

## Skill Version(s): <br>
3.4.1 (source: ClawHub release metadata; artifact frontmatter reports 3.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
