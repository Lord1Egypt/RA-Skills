## Description:

Check whether mission claims and deliverables are supported by reproducible evidence and explicit verification results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdjahid11978-design](https://clawhub.ai/user/mdjahid11978-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to assess whether mission completion, repository changes, test results, and external action claims have traceable supporting evidence. It produces a criterion-by-criterion status and calls out missing evidence and unresolved risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit conclusions may be mistaken for approval or proof that an external action occurred.

Mitigation: Keep audit findings separate from authorization and require a confirming result before reporting a commit, merge, deployment, or deletion.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/mdjahid11978-design/Jahids-skills/tree/main/skills/jahids-evidence-auditor)
- [ClawHub skill release](https://clawhub.ai/mdjahid11978-design/skills/jahids-evidence-auditor)
- [Publisher profile](https://clawhub.ai/user/mdjahid11978-design)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown evidence ledger and verification summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each criterion is marked PASS, FAIL, BLOCKED, or NOT_TESTED; missing evidence and unresolved items are reported.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
