## Description: <br>
jpocr extracts text from Japanese documents, screenshots, and scanned pages using local NDLOCR-Lite OCR, with support for printed Japanese, vertical Japanese text, and English text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realwaynesun](https://clawhub.ai/user/realwaynesun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run local OCR on Japanese images or document scans and return extracted text, JSON bounding boxes, or visualization images without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Attacker-controlled filenames or shell-like input may be mishandled by the wrapper script. <br>
Mitigation: Use trusted file paths, avoid passing attacker-controlled filenames, and prefer an update that quotes shell arguments or otherwise hardens the wrapper. <br>
Risk: The skill processes document images supplied by the user, which may contain sensitive content. <br>
Mitigation: Process only documents appropriate for the local environment and review output files before sharing them. <br>


## Reference(s): <br>
- [ClawHub jpocr release](https://clawhub.ai/realwaynesun/jpocr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [Plain text, JSON with bounding boxes, or visualization image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process one image or batch a directory; visualization output is saved to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
