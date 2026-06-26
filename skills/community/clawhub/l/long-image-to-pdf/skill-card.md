## Description: <br>
Slices long images/screenshots into overlapping segments and auto-arranges them into a paginated PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byronleeeee](https://clawhub.ai/user/byronleeeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other users can use this skill to convert long screenshots or tall image captures into paginated PDF documents. The skill runs a local Python script that slices the source image, arranges slices into pages, and reports the final PDF path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes user-provided images locally, which may include sensitive screenshots or captured content. <br>
Mitigation: Run it only on images the user intends to process locally, and choose an output directory the user controls. <br>
Risk: Intermediate image slices can remain on disk when cleanup is disabled. <br>
Mitigation: Use --cleanup by default; omit it only when the user explicitly wants to inspect or keep the generated slices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byronleeeee/long-image-to-pdf) <br>
- [Publisher profile](https://clawhub.ai/user/byronleeeee) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated PDF file and optional intermediate image slices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent normally uses --cleanup to remove generated intermediate slices unless the user asks to keep them.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
