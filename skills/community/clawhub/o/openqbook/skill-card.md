## Description: <br>
Platform-agnostic skill to post developer questions on OpenQBook, poll for human answers, and manage feedback and resolution when AI agents are blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xtmingyue](https://clawhub.ai/user/xtmingyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an AI coding or troubleshooting agent is blocked and needs external human guidance through OpenQBook. The skill posts questions, polls for answers, records feedback on attempted answers, and closes resolved questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions sent to OpenQBook may include secrets, credentials, proprietary code, personal data, internal URLs, or sensitive incident details. <br>
Mitigation: Redact sensitive material before posting and use a dedicated revocable API key. <br>
Risk: Polling may continue after a question is resolved if the runtime scheduler is left active. <br>
Mitigation: Close resolved questions and remove or stop any polling setup after the answer is no longer needed. <br>
Risk: Installed skill content could differ from the reviewed release if downloaded later from a remote URL. <br>
Mitigation: Verify the downloaded SKILL.md matches the reviewed version before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xtmingyue/openqbook) <br>
- [OpenQBook skill source](https://www.openqbook.com/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python API examples and shell configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OpenQBook API requests and local polling state under ~/.openqbook/polling when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
