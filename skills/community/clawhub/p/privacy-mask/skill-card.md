## Description: <br>
Mask, redact, anonymize and censor sensitive information in screenshots and images using local OCR, regex rules, and optional NER before images are shared. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users handling screenshots use this skill to detect and mask private data before image analysis or prompt submission. It supports privacy, compliance, secret detection, and data loss prevention workflows that require local redaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic prompt hooks may run broadly and modify images before submission without clear user confirmation. <br>
Mitigation: Confirm whether hook execution is opt-in, preview dry-run detections when possible, and avoid in-place edits unless the user explicitly requests them. <br>
Risk: Redaction quality depends on OCR, regex, and optional NER coverage, so sensitive data may be missed. <br>
Mitigation: Review dry-run detections, use custom configuration for domain-specific identifiers, and manually inspect masked images before sharing externally. <br>
Risk: The skill requires local dependencies such as tesseract, Python 3.10+, and the privacy-mask CLI. <br>
Mitigation: Verify required binaries and CLI installation before relying on the skill in a workflow. <br>


## Reference(s): <br>
- [Privacy Mask homepage](https://github.com/fullstackcrew-alpha/privacy-mask) <br>
- [ClawHub listing](https://clawhub.ai/fullstackcrew-alpha/privacy-mask) <br>
- [Publisher profile](https://clawhub.ai/user/fullstackcrew-alpha) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local redaction guidance and may result in masked image files written beside the input image or to a user-specified path.] <br>

## Skill Version(s): <br>
0.3.5 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
