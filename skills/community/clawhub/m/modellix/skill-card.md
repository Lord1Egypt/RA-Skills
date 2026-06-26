## Description: <br>
Integrates Modellix's unified API and CLI for asynchronous AI image and video generation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modellix](https://clawhub.ai/user/modellix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to select Modellix media models, submit image or video generation tasks, poll results, and retrieve generated resources through CLI-first or REST fallback workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Modellix API key for CLI or REST calls. <br>
Mitigation: Use a revocable, session-only MODELLIX_API_KEY by default and avoid exposing key values in command lines, logs, transcripts, screenshots, or committed files. <br>
Risk: Prompts and user-provided media URLs or file-derived content may be sent to Modellix during generation. <br>
Mitigation: Review prompts and media inputs before submission and use the skill only when Modellix media generation is intended. <br>
Risk: Installing the optional Modellix CLI globally adds a third-party executable to the user's environment. <br>
Mitigation: Verify the npm CLI package before global installation and use REST fallback when the CLI is unavailable or unsuitable. <br>


## Reference(s): <br>
- [Modellix Skill Page](https://clawhub.ai/modellix/modellix) <br>
- [Publisher Profile](https://clawhub.ai/user/modellix) <br>
- [Modellix Agent Quick Start](https://docs.modellix.ai/get-started.md) <br>
- [Modellix API Documentation](https://docs.modellix.ai/ways-to-use/api.md) <br>
- [Modellix CLI Documentation](https://docs.modellix.ai/ways-to-use/cli.md) <br>
- [Modellix Models Index](https://docs.modellix.ai/llms.txt) <br>
- [Capability Matrix](references/capability-matrix.md) <br>
- [CLI Playbook](references/cli-playbook.md) <br>
- [REST Playbook](references/rest-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json, code] <br>
**Output Format:** [Markdown guidance with CLI, REST, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit normalized Modellix task results containing mode, task ID, status, generated resource URLs, and raw submit/poll payloads.] <br>

## Skill Version(s): <br>
1.0.16 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
