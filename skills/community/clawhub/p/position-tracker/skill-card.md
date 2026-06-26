## Description: <br>
Keep track of positions across exchanges, brokers, or external systems, detect orphaned or phantom positions, and reconcile local state with external APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to add Python-based position lifecycle tracking, orphan detection, phantom cleanup, and reconciliation to bots or services that depend on external state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional cleanup behavior can affect real external positions or resources when connected to privileged APIs. <br>
Mitigation: Test with sandbox or read-only credentials first, use narrowly scoped API keys, and manually review orphan detections before enabling automatic cleanup. <br>
Risk: The local state file can contain sensitive position metadata. <br>
Mitigation: Protect the state directory with appropriate filesystem permissions and avoid storing secrets in position metadata. <br>
Risk: External API downtime, rate limits, or race conditions can delay or misclassify reconciliation results. <br>
Mitigation: Tune reconciliation intervals, add adapter-level retry and verification logic, and keep automatic reconciliation disabled until behavior is validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/position-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README.md](artifact/README.md) <br>
- [LIMITATIONS.md](artifact/LIMITATIONS.md) <br>
- [config_example.json](artifact/config_example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python, JSON, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces integration guidance and examples for local file-backed position state management.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
