## Description: <br>
Generate a PNG mind map from Markdown using free, center, or horizontal layout modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawyer-shi](https://clawhub.ai/user/sawyer-shi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to convert Markdown notes, outlines, or plans into local PNG mind map images with automatic, radial, or horizontal layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically download a CJK font from GitHub into a local cache on first run. <br>
Mitigation: Run it only where that network access is acceptable, or use an offline or patched copy that relies on bundled or system fonts. <br>
Risk: The runner saves the provided Markdown input locally alongside generated outputs, which can retain sensitive note content. <br>
Mitigation: Avoid sensitive Markdown unless the output directory is controlled, and delete generated Markdown copies when they are no longer needed. <br>


## Reference(s): <br>
- [Mind Map Skill Reference](artifact/reference.md) <br>
- [Mind Map Skill Examples](artifact/examples.md) <br>
- [CJK Font Download Source](https://raw.githubusercontent.com/sawyer-shi/mind-map-skill/main/resources/chinese_font.ttc) <br>
- [ClawHub Skill Page](https://clawhub.ai/sawyer-shi/mind-map-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Text] <br>
**Output Format:** [PNG image file, saved Markdown input file, and text run summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs under mind_map_output/YYYY-MM-DD/ by default unless flat output is selected.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
