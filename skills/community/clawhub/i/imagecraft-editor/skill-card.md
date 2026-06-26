## Description: <br>
Builds AI-powered image editing web applications that use StepFun's step-image-edit-2 API with a Flask backend and React frontend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuanjianghu](https://clawhub.ai/user/kaiyuanjianghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold an image editing web app with upload, feature selection, StepFun API calls, before/after comparison, and download support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images are sent to StepFun for editing. <br>
Mitigation: Use the skill only when users consent to third-party image processing and are told what service receives the images. <br>
Risk: The template stores uploaded and generated images without strong disclosure, deletion, or retention controls. <br>
Mitigation: Add visible consent, retention limits, and deletion controls before using the app with real user photos. <br>
Risk: A configurable STEPFUN_BASE_URL could send images and credentials to an unapproved endpoint. <br>
Mitigation: Restrict STEPFUN_BASE_URL to approved StepFun HTTPS endpoints and keep STEPFUN_API_KEY server-side. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaiyuanjianghu/imagecraft-editor) <br>
- [StepFun API base URL](https://api.stepfun.com/v1) <br>
- [StepFun Step Plan API base URL](https://api.stepfun.com/step_plan/v1) <br>
- [StepFun image edit endpoint](https://api.stepfun.com/v1/images/edit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code and shell command snippets plus project template files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a server-side STEPFUN_API_KEY and sends image payloads to the configured StepFun endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
