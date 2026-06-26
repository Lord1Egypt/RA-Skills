## Description: <br>
Render JSON schemas to images and generate schemas from prompts using declare-render and AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cai-zhuo](https://clawhub.ai/user/cai-zhuo) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and engineers use this CLI to render declare-render JSON schemas as PNG or JPG images, validate render-data schemas, or generate a schema from a prompt before rendering it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AI generation path depends on a materials-agents dependency that security evidence reports as missing local code. <br>
Mitigation: Verify the materials-agents dependency before installing or using the generate command. <br>
Risk: API credentials can be supplied on the command line and generation can use custom OpenAI-compatible base URLs. <br>
Mitigation: Prefer OPENAI_API_KEY from the environment and avoid untrusted custom base URLs or sensitive prompt content. <br>
Risk: Windows shell handling and untrusted prompt or file path strings may need extra caution. <br>
Mitigation: Review file paths and prompt strings before execution, especially on Windows. <br>


## Reference(s): <br>
- [Materials CLI on ClawHub](https://clawhub.ai/cai-zhuo/materials-cli) <br>
- [node-canvas installation guide](https://github.com/Automattic/node-canvas#installation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file-oriented outputs such as JSON schemas and PNG/JPG images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for CLI execution and OPENAI_API_KEY for AI schema generation.] <br>

## Skill Version(s): <br>
1.0.8 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
