## Description: <br>
Image Reader analyzes user-provided images with a multimodal model to extract OCR text, describe visual content, or provide mixed image analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonjoe246](https://clawhub.ai/user/simonjoe246) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to analyze screenshots or image files, extract visible text, and generate concise image descriptions through a configured multimodal API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, screenshots, and visible text are sent to the configured external multimodal API endpoint. <br>
Mitigation: Use the skill only with images approved for that provider, and avoid sensitive screenshots unless sharing has been reviewed and authorized. <br>
Risk: API credentials are configured through config.yaml. <br>
Mitigation: Replace the placeholder with a scoped key, restrict access to the configuration file, and avoid committing real credentials. <br>
Risk: Dependencies are declared with lower bounds rather than pinned versions. <br>
Mitigation: Pin and review dependency versions before use in sensitive or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simonjoe246/image-reader) <br>
- [Configured Volcengine-compatible API endpoint](https://ark.cn-beijing.volces.com/api/coding/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown returned from command-line or agent skill invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include extracted OCR text, visual descriptions, mixed image analysis, or error messages from the configured API call.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
