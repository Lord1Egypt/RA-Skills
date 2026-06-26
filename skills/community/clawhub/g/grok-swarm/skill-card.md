## Description: <br>
Grok Swarm gives coding agents a Grok 4.20 multi-agent bridge for codebase analysis, refactoring, code generation, and complex reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KHAEntertainment](https://clawhub.ai/user/KHAEntertainment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to send selected project files and prompts to a Grok-backed multi-agent bridge for security review, architecture analysis, refactoring, feature generation, tests, and reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected project files and prompts to OpenRouter/Grok. <br>
Mitigation: Review the file list and prompt before use, and do not include secrets, private data, or files that should not leave the local environment. <br>
Risk: The skill can discover local API credentials from environment variables, config files, or OpenClaw auth profiles. <br>
Mitigation: Keep API keys out of repositories and shared logs, restrict config file permissions, and rotate keys if they are exposed. <br>
Risk: The skill can write generated code blocks to local files. <br>
Mitigation: Use dry-run behavior first, constrain the output directory, and review generated changes before applying or committing them. <br>
Risk: The CLI includes an arbitrary shell execution option. <br>
Mitigation: Do not use the execute option unless you explicitly intend to run that exact command and have reviewed it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KHAEntertainment/grok-swarm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with optional code blocks, file-write summaries, shell command output, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter-compatible API key; may read selected local files, call a third-party model service, write generated files, and optionally run a provided shell command.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
