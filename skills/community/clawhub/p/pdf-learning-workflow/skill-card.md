## Description: <br>
Converts scanned PDF books into OCR text, chapter structure, study guides, learning notes, and HTML reading pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4zsz6jmmx6-source](https://clawhub.ai/user/4zsz6jmmx6-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert scanned PDF books into structured study materials, including OCR text, guide files, chapter notes, cropped assets, and browsable HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanned PDF page images are sent to an external GLM-OCR service. <br>
Mitigation: Use the skill only for documents where external processing by ZhipuAI/GLM-OCR is acceptable; avoid confidential, regulated, or copyright-sensitive files unless that transfer is approved. <br>
Risk: The workflow requires a GLM-OCR API key stored in a local configuration file. <br>
Mitigation: Store the key at ~/.config/glm-ocr/api_key with normal restricted local file permissions and do not share generated logs or files that may reveal operational details. <br>
Risk: Generated HTML loads KaTeX assets from jsDelivr. <br>
Mitigation: Review generated HTML before distribution and replace CDN assets with approved local or pinned assets if external CDN loading is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/4zsz6jmmx6-source/pdf-learning-workflow) <br>
- [ZhipuAI GLM-OCR service](https://bigmodel.cn) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown notes, HTML pages, shell commands, configuration steps, and local output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OCR chunks, merged Markdown, a guide, chapter structure, learning-note Markdown, cropped image assets, and HTML navigation pages.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
