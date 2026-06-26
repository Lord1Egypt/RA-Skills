## Description: <br>
Pill Counter Skill counts pills from images using a local OpenCV mode by default and an optional MiMo V2 Omni AI mode when an API key is configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsonxuan](https://clawhub.ai/user/johnsonxuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to count and classify pills in an image, generate a statistics table, and optionally save annotated image or CSV outputs. The local OpenCV path is suitable for regular pill layouts, while the optional AI mode can be used for more complex scenes when sharing the selected image with the MiMo API is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI mode uploads the selected pill image to Xiaomi MiMo, which may disclose medical details and consume paid API quota. <br>
Mitigation: Use the default local OpenCV mode for sensitive images, and enable --ai only when the user accepts the privacy and cost implications. <br>
Risk: OpenCV mode may miss pills in overlapping or complex scenes. <br>
Mitigation: Review the generated counts and annotated image, and consider AI mode only when the image can be shared with the configured provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsonxuan/pill-counter-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Command-line output as a text table or JSON, with optional CSV statistics and annotated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OpenCV mode runs locally by default; AI mode requires a configured MiMo API key and may use paid quota.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release metadata; artifact frontmatter reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
