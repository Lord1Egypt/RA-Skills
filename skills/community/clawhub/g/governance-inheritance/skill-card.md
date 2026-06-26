## Description: <br>
Governance Inheritance helps OpenClaw agents define, initialize, and validate hierarchical policies across organization, team, project, and session levels with inheritance, overrides, and conflict resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aakash2289](https://clawhub.ai/user/aakash2289) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up hierarchical governance policies for OpenClaw agents, initialize policy levels, validate policy chains, and reason about inherited allow, deny, and approval rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent governance policies and is intended to influence policy enforcement decisions. <br>
Mitigation: Review the generated policies before using them as an enforcement dependency and back up any existing GOVERNANCE_ROOT directory before running the initializer. <br>
Risk: The authoritative security summary notes internally inconsistent deny/allow inheritance rules. <br>
Mitigation: Test policy resolution on sample parent-deny and child-allow cases, and do not treat the skill as a reliable security boundary until precedence rules are clarified and covered by tests. <br>


## Reference(s): <br>
- [Policy Schema Reference](references/policy-schema.md) <br>
- [Inheritance Algorithm Reference](references/inheritance-algorithm.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline YAML, TypeScript, JSON, and bash examples, plus Python scripts that create or validate policy files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include persistent governance policy files under GOVERNANCE_ROOT when the initializer script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
