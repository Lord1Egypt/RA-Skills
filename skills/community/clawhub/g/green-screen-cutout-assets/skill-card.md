## Description: <br>
Generate green-screen raster subject assets with an image model and convert them into transparent PNGs with robust chroma-key cutout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[act-chao](https://clawhub.ai/user/act-chao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to create foreground bitmap assets such as pet stickers, character sprites, props, icons, collectibles, and UI decorations that need transparent backgrounds. It guides image generation on green-screen backgrounds, chroma-key cutout, QA review, and integration into project asset folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cutouts can retain green halos, lose fine subject details, or leave corners non-transparent. <br>
Mitigation: Inspect the JSON report and contact sheet before integration, rerun cutout settings when QA warnings appear, and regenerate source images when green subject details or edge shadows compromise the cutout. <br>
Risk: Generated assets can include unwanted text, watermarks, cropped body parts, or subject colors that conflict with chroma-key removal. <br>
Mitigation: Use the provided prompt constraints, keep source images padded and isolated, and reject candidates that fail the skill's visual QA rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/act-chao/skills/green-screen-cutout-assets) <br>
- [Server-resolved GitHub provenance](https://github.com/ACT-chao/green-screen-cutout-assets-skill/tree/master/green-screen-cutout-assets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python script invocations, file paths, and QA artifact descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides generation of transparent PNG assets, cutout reports, contact sheets, and project asset registry updates.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
