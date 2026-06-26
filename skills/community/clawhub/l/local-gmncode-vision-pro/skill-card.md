## Description: <br>
Provides agent workflows and scripts for batch image analysis, structured JSON output, screenshot and UI understanding, and resilient fallback vision processing backed by GMNCODE. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[io2077](https://clawhub.ai/user/io2077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when built-in image tools are unavailable or when workflows need batch image analysis, screenshot or UI understanding, and machine-readable vision results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected local images or screenshots to an external GMNCODE API, which can expose sensitive screenshots, documents, credentials, customer data, or internal UI captures. <br>
Mitigation: Use only with approved images and a trusted GMNCODE_API_KEY; redact sensitive content before analysis and avoid private or regulated data unless explicit approval is in place. <br>
Risk: The security review found insufficient user-facing disclosure and consent controls around external image uploads. <br>
Mitigation: Add clear upload warnings, an explicit opt-in step, file and path limits, and handling guidance before deploying this skill in shared or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/io2077/local-gmncode-vision-pro) <br>
- [GMNCODE Responses API endpoint](https://gmncode.cn/v1/responses) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured results can include summary, detected_entities, style, confidence, and uncertainty_notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
