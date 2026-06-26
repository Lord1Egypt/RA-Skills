## Description: <br>
Scans image folders and uses Gemini 2.0 Flash to analyze and categorize photos by composition, lighting, subject, mood, tone, style, and related photography attributes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrxolin](https://clawhub.ai/user/mrxolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, photographers, and content managers use this skill to batch-scan local image folders, classify photos, and generate structured analysis reports with a Gemini vision model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send selected local image contents to Gemini for analysis. <br>
Mitigation: Use it only on folders whose images are approved for external model processing, and avoid sensitive or regulated images. <br>
Risk: Folder scanning can process more images than intended. <br>
Mitigation: Run it against an explicit review folder and confirm the target path before execution. <br>
Risk: Proxy and API key settings affect where image analysis traffic is routed. <br>
Mitigation: Use trusted network settings and manage the Gemini API key through approved secret-handling practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrxolin/image-scanner-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mrxolin) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console report and optional JSON report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key for model-backed image analysis; without one, it falls back to filename-based basic classification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
