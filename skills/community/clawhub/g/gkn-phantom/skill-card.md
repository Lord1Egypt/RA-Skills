## Description:

GKN Phantom supports authorized penetration testing and security validation with scoped reconnaissance, vulnerability detection, PoC and exploit generation, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanguin37](https://clawhub.ai/user/yuanguin37)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and developers use this skill to run authorized penetration tests, security audits, and vulnerability validation against scoped staging, development, internal, or lab targets. It helps produce reproducible findings, PoCs, exploit artifacts, attack-path analysis, and security reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This is a powerful penetration-testing skill with real exploit generation and needs manual review before use.

Mitigation: Install only for controlled workflows with written authorization, explicit scope, and human review of generated PoCs and exploits before execution.

Risk: The quick-run path has weak runtime guard enforcement for broad or third-party targets.

Mitigation: Add an external scope guard, lower rate limits, and disable exploit generation, OOB behavior, memory, or session persistence features when they are not required.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/yuanguin37/GKN-Phantom)
- [ClawHub skill page](https://clawhub.ai/yuanguin37/skills/gkn-phantom)
- [Safety policy](references/safety_policy.md)
- [Data schemas](references/data_schemas.md)
- [Payload playbook](references/payload_playbook.md)
- [Advanced payload playbook](references/advanced_payload_playbook.md)
- [Script contracts](references/script_contracts.md)
- [Tool contracts](references/tool_contracts.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown reports, generated PoC/exploit code, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final outputs include summaries, risk scores, assets, validated findings, unverified leads, attack paths, recommendations, and execution logs.]

## Skill Version(s):

5.3.0 (source: artifact/SKILL.md frontmatter); ClawHub release version 0.1.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
