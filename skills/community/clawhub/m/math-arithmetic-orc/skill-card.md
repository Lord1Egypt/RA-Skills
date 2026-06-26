## Description: <br>
Recognizes K-12 arithmetic expressions in uploaded math images, including handwritten and printed equations, and returns structured OCR text results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzheigege](https://clawhub.ai/user/hzheigege) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract editable arithmetic text and detection details from K-12 math problem images, including vertical calculations, fractions, and equations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Math images or image URLs are sent to Tencent Cloud for OCR processing. <br>
Mitigation: Use the skill only with images appropriate for Tencent Cloud processing and follow applicable privacy or data-handling requirements. <br>
Risk: Tencent Cloud credentials are required to call the OCR API. <br>
Mitigation: Use a dedicated least-privilege Tencent Cloud OCR key and store it in platform secret storage or environment variables rather than normal parameters. <br>
Risk: The artifact depends on axios ^1.6.0. <br>
Mitigation: Pin or update axios to a vetted patched version before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hzheigege/math-arithmetic-orc) <br>
- [Tencent Cloud OCR API endpoint](https://ocr.tencentcloudapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, structured data] <br>
**Output Format:** [JSON-compatible object containing status, message, recognized text, detection metadata, rotation angle, raw response, and request ID.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud OCR credentials; optional settings can reject non-arithmetic images and include vertical-calculation intermediate results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
