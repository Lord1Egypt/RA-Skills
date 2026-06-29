## Description: <br>
Provides weighted scoring, rubrics, and decision-threshold patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and agents use this skill to define weighted criteria, score artifacts consistently, and map scores to review or approval decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad evaluation triggers may cause the skill to influence scoring, rubric, or quality-gate tasks beyond its intended context. <br>
Mitigation: Use it as a scoring and rubric aid, and require human review before applying outputs to consequential decisions. <br>
Risk: Reusable thresholds and rubrics may be mistaken for approval, hiring, moderation, compliance, or deployment policy. <br>
Mitigation: Treat generated evaluation structures as templates and adapt them to domain-specific policy, evidence requirements, and reviewer accountability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-evaluation-framework) <br>
- [Leyline homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Scoring Patterns](artifact/modules/scoring-patterns.md) <br>
- [Decision Thresholds](artifact/modules/decision-thresholds.md) <br>
- [Evaluation Rubric](artifact/modules/evaluation-rubric.md) <br>
- [Multi-Metric Evaluation Methodology](artifact/modules/multi-metric-evaluation-methodology.md) <br>
- [Quality Metrics](artifact/modules/quality-metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with YAML and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only evaluation framework; no code execution or data access.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
