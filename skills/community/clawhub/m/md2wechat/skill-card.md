## Description: <br>
Convert Markdown to WeChat Official Account HTML and guide related preview, draft, image generation, writing, and discovery workflows with the md2wechat CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geekjourneyx](https://clawhub.ai/user/geekjourneyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and publishing operators use this skill to route Markdown articles through md2wechat for WeChat formatting, local preview, draft creation, image-first posts, cover or infographic generation, style writing, and configuration discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft creation, image upload, publishing, or remote image generation can use configured md2wechat, WeChat, or image-provider credentials. <br>
Mitigation: Run those actions only when the user explicitly asks for them, and review commands involving upload, draft creation, publishing, or remote image generation before execution. <br>
Risk: Formatting workflows may produce modified Markdown that differs from the user's source article. <br>
Mitigation: Keep source Markdown read-only, write generated formatting to a temporary artifact, validate layout syntax, and require explicit confirmation before saving next to the source. <br>
Risk: CLI behavior, themes, providers, prompts, and layout modules can differ from stale documentation or memory. <br>
Mitigation: Use the md2wechat discovery commands for the current executable before choosing providers, themes, prompts, layout modules, or changed capabilities. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI JSON interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary formatted Markdown files and invoke md2wechat CLI actions when explicitly requested.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
