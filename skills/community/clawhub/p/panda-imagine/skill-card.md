## Description: <br>
panda-imagine is a multi-provider image generation skill that routes text prompts, reference-image requests, aspect-ratio settings, and batch jobs through OpenAI, Azure OpenAI, Google Gemini, OpenRouter, DashScope, MiniMax, Jimeng, Seedream, and Replicate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hash-panda](https://clawhub.ai/user/hash-panda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to generate and edit images through a single CLI across configured providers, including batch and reference-image workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are uploaded to the configured third-party image provider. <br>
Mitigation: Use only providers you trust, choose --provider explicitly for sensitive work, and avoid private reference images unless uploading them to that provider is acceptable. <br>
Risk: The Jimeng setup path includes an optional curl-to-bash installer. <br>
Mitigation: Independently verify the installer source or use a safer vendor-supported installation method before running it. <br>
Risk: Multiple configured API keys can cause provider auto-selection for paid or sensitive jobs. <br>
Mitigation: Set only the API keys needed for the intended workflow and specify --provider when cost, routing, or data handling matters. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/hash-panda/panda-skills#panda-imagine) <br>
- [First-time setup](references/config/first-time-setup.md) <br>
- [EXTEND.md configuration schema](references/config/preferences-schema.md) <br>
- [Jimeng CLI](https://jimeng.jianying.com/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; the script produces image files and can emit JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun or npx plus API credentials for the selected image provider; supports batch jobs and reference images where providers allow them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
