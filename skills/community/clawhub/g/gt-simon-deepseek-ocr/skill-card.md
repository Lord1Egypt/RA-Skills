## Description: <br>
Extract and return text content from images, screenshots, or scanned documents using DeepSeek OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sendream2002](https://clawhub.ai/user/Sendream2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from local image files, screenshots, and scanned documents when OCR output is needed in a workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime, command packaging, and documented entry points do not line up cleanly, so the installed entry point may not perform OCR as expected. <br>
Mitigation: Confirm which entry point will run before installation and require the maintainer to align the runtime, command name, script path, and documentation before routine use. <br>
Risk: The OCR path can send local image paths to a DeepSeek OCR endpoint selected by DEEPSEEK_OCR_HOST and DEEPSEEK_OCR_PORT. <br>
Mitigation: Use only a trusted OCR endpoint and review those environment variables before processing sensitive images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sendream2002/gt-simon-deepseek-ocr) <br>
- [Publisher profile](https://clawhub.ai/user/Sendream2002) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or plain text OCR results, depending on the active entry point.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JavaScript OCR path returns text, confidence, and model fields; the configured Python handler returns a placeholder text response.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; package.json lists 0.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
