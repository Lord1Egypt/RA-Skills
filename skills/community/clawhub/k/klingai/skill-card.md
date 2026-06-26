## Description: <br>
Kling AI helps agents run Kling video generation, image generation, subject management, and account quota workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klingai-dev](https://clawhub.ai/user/klingai-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to route agent requests to Kling AI for video generation, image generation, reusable subject management, and read-only account quota checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use account credentials to access a Kling account. <br>
Mitigation: Install only when account connection is intended, use a trusted machine, and protect or revoke stored credentials when needed. <br>
Risk: The skill can upload selected media to Kling AI. <br>
Mitigation: Review media inputs before submission and avoid providing sensitive files unless the upload is intended. <br>
Risk: Generation requests can spend Kling quota. <br>
Mitigation: Confirm generation intent before running costly jobs and avoid speculative retries. <br>
Risk: Subject management can delete Kling subjects. <br>
Mitigation: List and confirm subject IDs before deletion. <br>


## Reference(s): <br>
- [Kling AI Skill on ClawHub](https://clawhub.ai/klingai-dev/klingai) <br>
- [Kling AI Developer Docs (CN)](https://app.klingai.com/cn/dev/document-api) <br>
- [Kling AI Developer Docs (Global)](https://kling.ai/document-api/quickStart/productIntroduction/overview) <br>
- [API Reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown and CLI output with local file paths, task IDs, and links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit API calls that return generated media files after polling.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
