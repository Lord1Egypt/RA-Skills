## Description:

Harness Engineering is a Generator/Evaluator dual-agent coding workflow for programming tasks that need planning, coding, review, quality gates, and change audit records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure coding work into planning, implementation, independent review, revision, and delivery steps with auditable change records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically commit and push repository changes without a clear user approval checkpoint.

Mitigation: Require explicit user approval after reviewing the staged diff, commit message, remote URL, branch, and CI/CD or deployment effects before allowing any commit or push.

Risk: The skill may create .harness workflow files and Chinese-language planning or review reports in the repository.

Mitigation: Review generated .harness files and reports for project fit, confidentiality, and localization requirements before adopting them.

## Reference(s):

- [Harness Engineering Skill Definition](artifact/SKILL.md)
- [Evaluator SOP](artifact/skills/evaluator.md)
- [Quality Gates Template](artifact/templates/quality-gates.md)
- [Website Workflow Rules](artifact/rules/website-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/cindypapa/skills/openclaw-harness-engineering)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate .harness workflow files and Chinese-language planning or review reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
