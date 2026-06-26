## Description: <br>
Converts PDF files into JPEG page images with pdftoppm, supports optional page ranges, and can package generated JPGs into a zip archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luohongq](https://clawhub.ai/user/luohongq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and end users use this skill to convert full PDFs or selected page ranges into JPEG images and optionally bundle those images for sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local shell scripts and depends on locally installed poppler-utils/pdftoppm. <br>
Mitigation: Install and run it only in an environment where local shell execution and the dependency are acceptable. <br>
Risk: Generated JPEGs and zip archives can expose pages from sensitive PDFs in the target folder. <br>
Mitigation: Review the output directory and avoid running the scripts on sensitive documents unless the storage location is appropriate. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated local JPEG or zip files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires poppler-utils/pdftoppm; generated JPEGs and zip archives are written next to the supplied PDF unless an archive path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
