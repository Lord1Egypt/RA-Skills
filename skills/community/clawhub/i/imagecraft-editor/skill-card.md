## Description:

Build AI-powered image editing web applications with StepFun's step-image-edit-2 API for photo restoration, portrait retouching, landscape color grading, and artistic style transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuanjianghu](https://clawhub.ai/user/kaiyuanjianghu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external builders use this skill to create a Flask and React image editing application that uploads images, sends them to StepFun's image editing API, and returns downloadable edited results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive photos may be uploaded, stored locally, and sent to a third-party image processing API.

Mitigation: Disclose third-party processing to users, delete originals and results when no longer needed, and authenticate or expire image URLs.

Risk: API keys and outbound image requests can be exposed or misused if the template is deployed without hardening.

Mitigation: Keep the StepFun API key server-side, allowlist StepFun API hosts, add upload size and rate limits, and update or lock dependencies.

Risk: Development defaults can increase exposure if used directly in production.

Mitigation: Disable Flask debug mode and review the template before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuanjianghu/skills/imagecraft-editor)
- [Publisher profile](https://clawhub.ai/user/kaiyuanjianghu)
- [StepFun API base URL](https://api.stepfun.com/v1)
- [StepFun Step Plan API base URL](https://api.stepfun.com/step_plan/v1)
- [StepFun image edit endpoint](https://api.stepfun.com/v1/images/edit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration values, and project template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local web app template with a Flask backend, Vite React frontend, image upload flow, API integration, and download path for generated images.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontend package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
