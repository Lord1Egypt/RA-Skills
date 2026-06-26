## Description: <br>
MOSES Governance is a constitutional governance harness for AI agents that provides modes, postures, roles, an audit chain, lineage custody, signing gates, and commitment verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add a governance layer around agent actions, including policy checks, role and posture controls, audit logging, lineage checks, and optional signing or external review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer agent workflow and persist local governance or audit records. <br>
Mitigation: Install it only when a broad governance layer is desired, and review the state directories and audit behavior before use. <br>
Risk: Optional referee and witness features can send derived task or governance data externally. <br>
Mitigation: Keep REFEREE_ENABLED and MOSES_WITNESS_ENABLED disabled unless the endpoint is trusted and the data sharing is acceptable. <br>
Risk: The security evidence says this release should not be treated as a strong boundary for approvals, rollback, presence, audit non-repudiation, or high-value signing. <br>
Mitigation: Use independent controls for high-value actions and verify approvals, signatures, audit handling, and headless behavior outside the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sunrisesillneversee/moses-governance) <br>
- [Publisher profile](https://clawhub.ai/user/sunrisesillneversee) <br>
- [MOSES project site](https://mos2es.io) <br>
- [Zenodo record](https://zenodo.org/records/18792459) <br>
- [MOSES Governance Modes](references/modes.md) <br>
- [MOSES Posture Controls](references/postures.md) <br>
- [MOSES Role Hierarchy](references/roles.md) <br>
- [Ghost Token Specification](references/ghost-token-spec.md) <br>
- [Falsifiability](references/falsifiability.md) <br>
- [The Shannon Extension](references/shannon-extension.md) <br>
- [The Lattice Governance Model](references/lattice-governance.md) <br>
- [Lineage Custody Clause](LINEAGE.md) <br>
- [Constitutional Amendment Format](AMENDMENT-FORMAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, governance records, JSON-style audit artifacts, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local governance state and audit records under configured OpenClaw state directories; optional external reporting is off by default.] <br>

## Skill Version(s): <br>
0.5.10 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
