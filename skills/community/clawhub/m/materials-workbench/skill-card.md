## Description: <br>
Materials editor workbench - React UI and Express server to render JSON schemas to images and generate schemas with AI (declare-render + materials-agents). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cai-zhuo](https://clawhub.ai/user/cai-zhuo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and designers use this skill to run a local materials workbench for creating, editing, previewing, and downloading declarative canvas images. It supports AI-assisted generation or refinement of RenderData schemas when an OpenAI-compatible API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local server uses an OpenAI-compatible API key for AI-assisted schema generation. <br>
Mitigation: Configure credentials only in the local server environment and use a provider, base URL, and model that meet the user's data-handling requirements. <br>
Risk: Attached images may be uploaded to PICUI when image upload support is enabled. <br>
Mitigation: Avoid uploading sensitive or proprietary images unless PICUI and the configured retention settings are acceptable. <br>
Risk: Core AI behavior depends on unbundled local code. <br>
Mitigation: Review or vendor the missing local dependencies before relying on the workbench. <br>
Risk: The security evidence recommends upgrading Vite. <br>
Mitigation: Update Vite and rebuild the client before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cai-zhuo/materials-workbench) <br>
- [Publisher Profile](https://clawhub.ai/user/cai-zhuo) <br>
- [PICUI Image Hosting](https://picui.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment configuration, and RenderData JSON or code-oriented edits when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and OPENAI_API_KEY for AI features; PICUI_TOKEN is optional for image uploads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
