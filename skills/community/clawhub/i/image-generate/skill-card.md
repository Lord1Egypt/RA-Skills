## Description: <br>
Generates images from a clear text prompt using the included image_generate.py script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangsiyuan123123](https://clawhub.ai/user/zhangsiyuan123123) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agents use this skill to turn text prompts into generated images through the bundled Volcengine Ark image-generation script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to an external image-generation provider. <br>
Mitigation: Avoid entering secrets, confidential data, or sensitive personal data in prompts. <br>
Risk: Generated images are saved to the configured local download directory. <br>
Mitigation: Set IMAGE_DOWNLOAD_DIR only to a directory where generated image files should be written. <br>
Risk: The script requires an external provider credential. <br>
Mitigation: Use a scoped Ark or Volcengine API key and provide it through the documented environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangsiyuan123123/image-generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text status messages and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses prompt text plus API key and download-directory environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
