## Description:

Helps agents analyze, plan, propose, and verify contractual AWS Glue workflow and trigger changes without performing live AWS execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kansodata](https://clawhub.ai/user/kansodata)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud platform engineers and developers use this skill to manage conceptual AWS Glue workflow and trigger changes through structured diagnosis, reversible planning, contractual change proposals, and evidence-based verification without exposing credentials or executing against AWS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect the skill to apply AWS Glue changes directly or accept AWS credentials.

Mitigation: Use it only for contractual planning and verification; do not provide credentials or request SDK/runtime AWS execution.

Risk: Plans can be incomplete when current state, acceptance criteria, or rollback details are missing.

Mitigation: Require explicit scope, evidence, acceptance criteria, and rollback details; return degraded or rejected when inputs are insufficient.

Risk: Requests involving Glue jobs, crawlers, plugins, persistence, or external APIs are outside the stated scope.

Mitigation: Reject mixed or out-of-scope requests fail-closed and limit actions to workflows and triggers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kansodata/skills/kansodata-glue-operator)
- [Skill scope](artifact/docs/scope.md)
- [Operational examples](artifact/docs/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured YAML-like Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contractual outputs only; no live AWS execution, credential handling, persistence, plugins, SDK runtime, or external API calls.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
