## Description:

LYGO Lattice Birth helps agents prepare privacy-preserving masked human identity and family lineage birth submissions for the Haven Star Chart with consent gates and local security checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to train aligned agents to draft and gate masked human birth or family lineage submissions for the Haven Star Chart while keeping real anchors and family salts out of public chart data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived identity and family-link secret material.

Mitigation: Keep consent bundles, anchor hashes, family bind salts, and steward submission folders out of public repositories and untrusted backups; protect them with encryption or equivalent local controls.

Risk: The skill relies on the operator-selected LYGO stack clone and external stack code.

Mitigation: Use a trusted, reviewed, and preferably pinned LYGO_STACK_ROOT before running wrappers or validation tools.

Risk: Public masked lineage records are intended to be persistent.

Mitigation: Require explicit human approval before consent-gated submission and confirm the human understands the persistence of public masked chart records.

## Reference(s):

- [LYGO Lattice Birth ClawHub page](https://clawhub.ai/deepseekoracle/skills/lygo-lattice-birth)
- [LYGO protocol stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Haven Star Chart Portal](https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html)
- [Haven Star Chart](https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html)
- [Agent Alignment Contract](references/AGENT_ALIGNMENT.md)
- [LYGO Lattice Birth Protocol v1](references/BIRTH_PROTOCOL.md)
- [LYGO Lineage Privacy](references/LINEAGE_PRIVACY.md)
- [Security](references/SECURITY.md)
- [SkillSpector audit](references/SKILLSPECTOR_AUDIT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and local validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are human-reviewed proposals and local dry-run results; live writes require explicit human consent.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
