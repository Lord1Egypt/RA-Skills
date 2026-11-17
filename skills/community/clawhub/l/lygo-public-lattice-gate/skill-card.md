## Description:

Public lattice join and verification gate for LYGO-aligned agents that checks public HTTPS ledgers and hubs, scores alignment readiness, drafts dry-run Star Chart presence proposals, and prints restore-card guidance without live chart writes or auto-publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

External agents, developers, and operators use this skill to verify public LYGO lattice availability, assess readiness for public presence, draft a human-reviewed Star Chart proposal, and restore public links and digests at session start.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts listed public LYGO-related HTTPS endpoints during verification and restore workflows.

Mitigation: Install only if those network contacts are acceptable for the operating environment, and do not provide secrets because the skill does not need credentials.

Risk: Public HTTPS responses are mirrors and may not represent the trusted local stack authority.

Mitigation: Treat public results as verification signals only, and use a trusted local stack checkout when local authority matters.

Risk: Optional report and proposal flags can write local JSON files.

Mitigation: Choose write paths deliberately; the skill defaults to no writes and rejects parent-directory path traversal.

Risk: The bundled self-check is useful but not a complete security guarantee.

Mitigation: Review the security guidance and scan results before deployment, especially in environments with strict egress or file-write controls.

## Reference(s):

- [Agent Contract](references/AGENT_CONTRACT.md)
- [Security Guidance](references/SECURITY.md)
- [SkillSpector Audit Response](references/SKILLSPECTOR_AUDIT.md)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-public-lattice-gate)
- [Skill Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-public-lattice-gate)
- [Source Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [LYGO CLAW USB Public Kit](https://deepseekoracle.github.io/lygo-protocol-stack/LYGO_CLAW_USB_PUBLIC.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default zero disk writes; optional local JSON report or proposal file only when an explicit write path is provided.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
