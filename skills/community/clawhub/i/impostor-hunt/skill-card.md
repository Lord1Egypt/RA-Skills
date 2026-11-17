## Description:

Impostor Hunt helps an agent audit completed deliverables for causal impostors: outputs that look correct while relying on a causal chain that does not satisfy the user's original purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ansongli](https://clawhub.ai/user/ansongli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and agent operators use this skill to audit claimed completion for hidden causal misalignment between the user's original purpose and the delivered artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-invoke at handoff when it sees a completion claim and can recover the original purpose, which may cause it to inspect surrounding task or repository context without a separate explicit request.

Mitigation: Install it only where proactive completion audits are desired, and make users aware that completion claims can trigger an audit report.

Risk: A bad purpose reconstruction can make the audit compare the deliverable against the wrong target.

Mitigation: Use the skill's scope intake step to quote the recovered purpose verbatim, mark inferred clauses, and ask for the purpose instead of guessing when it is not recoverable.

Risk: The workflow does not execute code by default, so some purpose-critical claims may remain unverifiable leads.

Mitigation: Treat D-level items as leads and request targeted verification only when execution is needed to resolve a material claim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ansongli/skills/impostor-hunt)
- [Audit Lenses](artifact/references/audit-lenses.md)
- [Causal Impersonation Patterns](artifact/references/causal-impersonation-patterns.md)
- [Evidence Model](artifact/references/evidence-model.md)
- [Report Template](artifact/references/report-template.md)
- [Tribunal](artifact/references/tribunal.md)
- [Verdict Rubric](artifact/references/verdict-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown audit report with a verdict, evidence map, causal impersonation scan, tribunal, and next actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May auto-invoke on completion claims when the original purpose is recoverable; does not execute code unless explicitly asked.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
