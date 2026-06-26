## Description: <br>
Token usage logging, alerting, and context-compression utilities for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gerhardvr26](https://clawhub.ai/user/gerhardvr26) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to track per-call token usage, normalize timestamps, alert on high-token calls, and summarize large contexts before sending them to an LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token usage logs can contain sensitive usage metadata. <br>
Mitigation: Choose the log folder deliberately, restrict access to generated logs, and treat them as sensitive operational records. <br>
Risk: The interceptor and summarizer are examples and are not a secret-redaction layer. <br>
Mitigation: Review and adapt scripts before wiring them into a message pipeline, and use a separate reviewed redaction process for secrets. <br>
Risk: The bundled systemd unit can run a background service if manually enabled. <br>
Mitigation: Enable the service only after review, correct the local paths, and run it under a least-privileged local user. <br>


## Reference(s): <br>
- [Example systemd service](references/systemd/token-interceptor.service.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts and JSON configuration; runtime utilities emit JSONL logs, text alerts, and text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default configuration uses UTC timestamps, ./skills/logs, and optional context summarization settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
