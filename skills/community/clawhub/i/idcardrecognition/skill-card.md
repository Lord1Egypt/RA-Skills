## Description: <br>
对身份证等证件图 OCR，返回姓名、号码等字段。当用户说：身份证照片识别一下信息、证件图转文字，或类似证件 OCR 时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to process authorized identity document images through JisuAPI OCR and return structured fields such as name, birth date, address, and document number. It is suitable for workflows that need document text extraction with privacy-aware summarization or redaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Identity document images and extracted personal details are sent to JisuAPI for OCR. <br>
Mitigation: Use the skill only for documents the user is authorized to process, and redact or avoid sharing full ID numbers, addresses, and portrait data unless necessary. <br>
Risk: The JISU_API_KEY environment variable grants access to a third-party API. <br>
Mitigation: Store the key in a protected environment variable, do not include it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: The skill can read local image files supplied by path from the current workspace. <br>
Mitigation: Provide only intended document image paths; the script rejects absolute paths and parent-directory traversal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/idcardrecognition) <br>
- [JisuAPI ID Card Recognition documentation](https://www.jisuapi.com/api/idcardrecognition/) <br>
- [JisuAPI provider homepage](https://www.jisuapi.com/) <br>
- [JisuAPI recognition endpoint](https://api.jisuapi.com/idcardrecognition/recognize) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON result objects or error objects, with optional natural-language summaries by the calling agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; accepts a local workspace-relative image path or a base64 image string plus a required typeid.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
