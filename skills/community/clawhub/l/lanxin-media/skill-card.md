## Description: <br>
Lanxin Media enables Lanxin image and file sending by emitting <lximg> and <lxfile> tags for supported paths or URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamdacai](https://clawhub.ai/user/iamdacai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and Lanxin users use this skill when they need an agent to hand off one image or file for Lanxin media sending with the platform-specific lximg or lxfile tag format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers and no-refusal instructions may cause the agent to emit Lanxin upload-style tags unintentionally. <br>
Mitigation: Enable the skill only where Lanxin media sending is expected, and confirm the file path or URL, destination, and sensitivity before acting on any lximg or lxfile output. <br>
Risk: The skill can request transmission of local file paths or external URLs. <br>
Mitigation: Review each referenced file or URL before upload and avoid sending confidential, regulated, or unintended content. <br>
Risk: Lanxin media constraints may reject unsupported or oversized files. <br>
Mitigation: Check file type and keep files within the documented 2 MB limit before using the emitted tag. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iamdacai/lanxin-media) <br>
- [Publisher profile](https://clawhub.ai/user/iamdacai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text containing Lanxin media tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs at most one image or file tag per action; supported files are limited by the skill to 2 MB and png, jpg, jpeg, pdf, doc, docx, xls, xlsx, and txt formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
