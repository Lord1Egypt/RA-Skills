## Description: <br>
model-troubleshooter diagnoses OpenClaw model and provider failures from configuration and logs, then proposes or applies configuration, credential, provider, retry, and verification fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viratkumar123](https://clawhub.ai/user/viratkumar123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot OpenClaw model, provider, API key, rate limit, timeout, streaming, and endpoint failures. It helps inspect local configuration and logs, identify likely root causes, recommend or apply fixes, and report verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect model and gateway configuration or logs that may contain credentials or sensitive operational details. <br>
Mitigation: Run a dry run first, redact secrets, and limit shared output to non-sensitive diagnostics. <br>
Risk: The skill may change model, provider, or gateway settings or restart services while troubleshooting. <br>
Mitigation: Require explicit approval before patches or restarts, keep a configuration backup, and verify behavior after each change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/viratkumar123/model-troubleshooter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, configuration changes, diagnostic summaries, and verification notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should redact secrets and distinguish dry-run recommendations from approved changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
