## Description: <br>
基于提供的图片或物料，自动提取文本与结构，生成符合标准、可直接开发执行的互联网产品需求文档（PRD）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sssssHaoa](https://clawhub.ai/user/sssssHaoa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and product teams use this skill to turn supplied screenshots, diagrams, architecture notes, business flows, and other materials into structured PRD Markdown grounded in the provided source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input screenshots, diagrams, and documents may contain secrets or confidential business details. <br>
Mitigation: Review and redact materials before use; provide only approved artifacts to OCR or vision tooling. <br>
Risk: OCR or vision extraction errors can lead to incorrect PRD requirements or missed relationships. <br>
Mitigation: Review the generated PRD against the original materials before product, design, development, or test work depends on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sssssHaoa/material-to-prd) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown PRD document using a fixed Chinese PRD template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounded only in user-provided materials and OCR or vision extraction results; no invented requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
