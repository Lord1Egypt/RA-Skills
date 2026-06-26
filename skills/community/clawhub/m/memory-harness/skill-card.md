## Description: <br>
Runtime-enforced memory harness for OpenClaw that implements staged recall, intent classification, entity detection, memory compression, and status tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taka3693](https://clawhub.ai/user/taka3693) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when prior conversation or project context should be recalled, compressed, logged, and checked before execution-like work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically recall, log, or persist sensitive user and project context, including raw user text. <br>
Mitigation: Avoid using it with secrets, regulated data, personal data, or confidential work unless logging, retention, writeback, and deletion controls are reviewed and constrained. <br>
Risk: Pre-execution recall can inject prior constraints or context into later work, which may be stale or low confidence. <br>
Mitigation: Review recalled context before relying on it for file edits, code generation, architecture decisions, or configuration changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/taka3693/memory-harness) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON decisions, compact text digests, and structured log lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recall output is deduplicated and capped to a small bounded digest.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
