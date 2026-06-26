## Description: <br>
Diagnoses and helps fix mimo-v2.5-pro and related mimo model API failures, including 400 Param Incorrect responses, rejected request schemas, tool-calling payload issues, and model configuration problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot OpenClaw requests to mimo models, validate API connectivity and tool-calling behavior, inspect model configuration, and apply targeted configuration fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic commands read local OpenClaw configuration and call the configured provider endpoint with an API key. <br>
Mitigation: Confirm the configured baseUrl is trusted, keep API keys private, and redact diagnostic output before sharing it. <br>
Risk: Configuration repair snippets can modify ~/.openclaw/openclaw.json and gateway restarts can change runtime model behavior. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before applying edits and review the intended changes before restarting the gateway. <br>


## Reference(s): <br>
- [mimo API error reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic commands, curl requests, log-search commands, and OpenClaw configuration edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
