## Description: <br>
DeepSeek lets an agent use OOMOL's oo CLI to call DeepSeek chat and message APIs, inspect models, and check account balance through a connected OOMOL account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to invoke DeepSeek chat completions or messages, list models, or check balance through an OOMOL-connected DeepSeek account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may rely on remote shell installer commands for the oo CLI. <br>
Mitigation: Review the installer first or manually install the oo CLI from official documentation before running setup commands. <br>
Risk: DeepSeek requests and credentials are mediated by OOMOL. <br>
Mitigation: Install only when that intermediary model is acceptable, and confirm prompts or payloads before sending them. <br>
Risk: The oo CLI authority can be broader than the listed DeepSeek actions. <br>
Mitigation: Inspect the live action schema before each payload and require explicit confirmation for write or destructive actions. <br>


## Reference(s): <br>
- [DeepSeek Platform](https://platform.deepseek.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector actions; write actions require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
