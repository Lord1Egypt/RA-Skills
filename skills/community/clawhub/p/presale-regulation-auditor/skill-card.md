## Description:

Audit regulation freshness and update policy-driven controls without hardcoding. Use when checking if sales/process regulations are outdated, inconsistent with operations, or need config-level updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsiomo](https://clawhub.ai/user/dtsiomo)

### License/Terms of Use:


## Use Case:

Sales operations, compliance, and policy engineers use this skill to audit whether presale regulations and operational controls are stale, conflicting, or non-executable, then draft config-level updates and rollout recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may expose internal regulations, incident history, and policy configuration details to the agent.

Mitigation: Limit inputs to the specific audit scope and avoid sharing unrelated sensitive material.

Risk: Proposed config diffs could change policy controls if applied without review.

Mitigation: Review proposed diffs with responsible owners and roll out approved changes in low-risk stages.

## Reference(s):

- [Regulation Check Workflow](references/regulation-check-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/dtsiomo/skills/presale-regulation-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown report with a staleness matrix, proposed config diffs, backward-compatibility notes, and rollout recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposals for review; it does not execute changes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
