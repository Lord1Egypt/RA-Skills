## Description: <br>
governance-guard enforces structural authority separation for autonomous agent actions through a three-phase PROPOSE, DECIDE, PROMOTE governance pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devongenerally-png](https://clawhub.ai/user/devongenerally-png) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to gate write, execute, network, create, and delete actions through deterministic policy evaluation before execution. It also provides policy presets and a local witness log for auditing governance decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy rules may approve, deny, or escalate the wrong actions if their patterns do not match the operator's environment. <br>
Mitigation: Review policy patterns before relying on them and prefer the standard or strict presets for sensitive environments. <br>
Risk: The local witness log can retain action targets, parameters, and user instructions. <br>
Mitigation: Install the skill only where a local audit trail is desired and handle ~/.openclaw/governance/witness.jsonl according to the data sensitivity of recorded actions. <br>


## Reference(s): <br>
- [Policy File Schema](references/policy-schema.md) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [ClawHub Release Page](https://clawhub.ai/devongenerally-png/governance-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON verdicts, audit text, and Markdown-ready guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Governance data is stored locally under ~/.openclaw/governance/ when the skill is used as documented.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
