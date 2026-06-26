## Description: <br>
Lightweight two-stage input safety guard for agents. Use this skill when an agent must screen user input before answering, block prompt injection or prompt leakage attempts, classify risky requests, and either return a safe answer or an interception response. The workflow is stage1 deterministic prefilter plus stage2 agent-native semantic review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywingswang](https://clawhub.ai/user/skywingswang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to screen raw user input before an agent answers, combining deterministic prompt-safety rules with agent-native semantic review. It is suited for flows that need configurable blocking, review, and safe-response routing before downstream prompt construction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default, strict, and relaxed profiles can block normal prompt-security discussions or trusted development workflows if left untuned. <br>
Mitigation: Review the rule profiles before installing, test them against the target agent flow, and choose or adjust the profile that fits the deployment context. <br>
Risk: The guard inspects raw user messages, which may include sensitive user-provided content. <br>
Mitigation: Ensure host classifiers, telemetry, and logs handle user input according to the deployment's privacy and retention requirements. <br>


## Reference(s): <br>
- [Input Safety Guard on ClawHub](https://clawhub.ai/skywingswang/input-safety-guard) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Default rules profile](artifact/config/default_rules.yaml) <br>
- [Strict rules profile](artifact/config/default_rules.strict.yaml) <br>
- [Relaxed rules profile](artifact/config/default_rules.relaxed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Plain text replies with structured safety decision metadata and configurable rule profiles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can return safety-only decisions, full handling metadata, or final user-visible text depending on the runtime entry point.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
