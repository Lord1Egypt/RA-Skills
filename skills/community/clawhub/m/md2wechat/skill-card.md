## Description: <br>
md2wechat helps agents use the md2wechat CLI to convert Markdown into WeChat Official Account HTML and manage previews, draft uploads, image generation plans, title suggestions, style writing, and humanizing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geekjourneyx](https://clawhub.ai/user/geekjourneyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and publishing operators use this skill to route WeChat article formatting, preview, draft, image, title, and style-polishing requests through the md2wechat CLI while checking readiness before side-effecting actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft creation, uploads, and remote image generation can produce external side effects when credentials are configured. <br>
Mitigation: Use inspect and preview workflows first, and only run upload, draft, or remote generation commands after the user explicitly asks for that action. <br>
Risk: Provider, theme, prompt, or layout assumptions can become stale relative to the installed md2wechat CLI. <br>
Mitigation: Run the narrow discovery command needed for the task, such as version, capabilities, list, show, doctor, or the embedded skill read command, before choosing modes or resources. <br>
Risk: Title suggestions, image plans, and style-writing flows may be mistaken for final publishing intent. <br>
Mitigation: Treat generated titles, prompt intents, and rewritten text as candidates for review, and do not write back, upload, or create drafts until the user approves. <br>


## Reference(s): <br>
- [ClawHub md2wechat listing](https://clawhub.ai/geekjourneyx/skills/md2wechat) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of temporary formatted Markdown, local previews, prompt intents, draft/upload commands, and configuration checks; upload, draft, and remote image-generation actions require explicit user request and appropriate credentials.] <br>

## Skill Version(s): <br>
2.9.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
