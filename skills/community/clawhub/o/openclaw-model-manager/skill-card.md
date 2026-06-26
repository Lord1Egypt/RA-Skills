## Description: <br>
Model Manager helps OpenClaw users add, remove, update, inspect, switch, and connectivity-test model and provider configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[the2015](https://clawhub.ai/user/the2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to maintain openclaw.json model and provider settings, switch the primary model, and diagnose model API connectivity or status-code issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete or alter live OpenClaw model, provider, alias, and default-model configuration entries, which could disrupt future agent behavior. <br>
Mitigation: Review the exact openclaw.json changes before applying them, back up the file first, and confirm no aliases or defaults still reference removed models or providers. <br>
Risk: Connectivity checks send test requests to configured model providers and may surface authentication, quota, or upstream-service issues. <br>
Mitigation: Use minimal test requests, keep rollback instructions available, and interpret 401, 403, 429, 400, and 5xx responses using the documented status-code guidance. <br>


## Reference(s): <br>
- [Model Info Reference](references/model-info.md) <br>
- [ClawHub release page](https://clawhub.ai/the2015/openclaw-model-manager) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON and PowerShell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-facing configuration guidance, status summaries, and restart or connectivity-test instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
