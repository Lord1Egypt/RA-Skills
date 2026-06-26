## Description: <br>
Generate images with an OpenAI-compatible image provider such as happy/gpt-image-2, with retries and bounded batch concurrency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to generate single images or bounded-concurrency image batches through a configured OpenClaw image provider, with generated files and JSON run results written locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to the configured external image provider. <br>
Mitigation: Use only trusted providers and avoid submitting secrets, regulated personal data, or confidential material unless that provider is approved for the data. <br>
Risk: Prompts, generated images, JSON results, and logs are stored in local run or batch directories. <br>
Mitigation: Review local retention practices, restrict filesystem access as appropriate, and remove generated run directories when the data no longer needs to be retained. <br>
Risk: The skill requires provider credentials through the local OpenClaw configuration. <br>
Mitigation: Configure least-privilege API keys, keep credentials out of prompts and source files, and rotate keys if logs or configuration are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/happy-img2-direct) <br>
- [Publisher profile](https://clawhub.ai/user/jerryxn) <br>


## Skill Output: <br>
**Output Type(s):** [files, JSON, shell commands, configuration] <br>
**Output Format:** [PNG image files with JSON status and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-image generation and bounded batch execution with retries; generated prompts, outputs, and logs are retained in local run directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
