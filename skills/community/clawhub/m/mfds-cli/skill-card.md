## Description: <br>
MFDS CLI lets agents query Korean Ministry of Food and Drug Safety public drug APIs for product permissions, consumer drug information, DUR contraindications, and recall or sale-stop alerts, returning normalized JSONL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, healthcare data teams, and medication-safety agent builders use this skill to query MFDS drug, DUR, and recall data from data.go.kr and feed normalized records into pharmacy AI workflows, prescription review, or Korean healthcare data pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MFDS service keys and medication search terms may be exposed if users share logs or full request URLs. <br>
Mitigation: Keep MFDS_API_KEY in the environment or a secret manager, avoid printing full URLs, and redact keys and medication terms before sharing logs. <br>
Risk: The endpoint override can direct requests away from the intended MFDS public API host if untrusted input controls it. <br>
Mitigation: Use the default endpoints for normal operation and allow --endpoint only from trusted configuration. <br>
Risk: Medication-safety outputs can be incomplete or stale if upstream MFDS data, rate limits, or query choices omit relevant records. <br>
Mitigation: Treat results as source data for review rather than final clinical advice, check timestamps and recall windows, and validate important decisions against authoritative MFDS records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloepark85/mfds-cli) <br>
- [Publisher profile](https://clawhub.ai/user/chloepark85) <br>
- [data.go.kr](https://www.data.go.kr) <br>
- [Skill reference](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSONL by default, with optional JSON or XML passthrough; documentation examples use Markdown with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MFDS_API_KEY and makes outbound HTTPS requests to data.go.kr MFDS public API endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
