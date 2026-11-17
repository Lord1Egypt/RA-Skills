## Description:

Use when mapping patent claims to products, analyzing patent infringement, or preparing freedom-to-operate analyses. Compares patent claims against product features for biotech and pharmaceutical IP assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IP analysts, and legal operations teams use this skill to map patent claim elements to biotech or pharmaceutical product features for preliminary infringement and freedom-to-operate analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent infringement and freedom-to-operate outputs may be incomplete, preliminary, or legally incorrect.

Mitigation: Treat generated patent-risk output as preliminary analysis and require qualified legal review before acting on it.

Risk: The artifact documentation includes stale claim_mapper.py examples that do not match the packaged script path.

Mitigation: Use scripts/main.py for CLI execution or correct the stale examples before installing or publishing the skill.

Risk: The requirements file declares an unnecessary dataclasses dependency for modern Python versions.

Mitigation: Remove the dependency or pin it deliberately during packaging review.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/patent-claim-mapper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional JSON analysis reports from the packaged CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI execution can write an infringement_report.json file containing risk level, risk score, claim mappings, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
