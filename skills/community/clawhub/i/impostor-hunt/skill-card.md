## Description: <br>
Audits finished deliverables for causal impostors: outputs that look correct but were produced by a causal chain that does not satisfy the user's original purpose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ansongli](https://clawhub.ai/user/ansongli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill after completion is declared to compare the delivered artifact against the user's recoverable purpose and decide whether the result is causally aligned, suspected impersonation, confirmed impersonation, or undecidable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger broadly during closeout review. <br>
Mitigation: Use it in trusted development workspaces and require the original user purpose to be recoverable before acting on an automatic audit. <br>
Risk: Full-access modes or fallback reviewers may expose diffs or untracked file contents to review tools. <br>
Mitigation: Disable yolo/full-access mode and fallback reviewers unless that level of local review is explicitly intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ansongli/impostor-hunt) <br>
- [Audit Lenses](references/audit-lenses.md) <br>
- [Causal Impersonation Patterns](references/causal-impersonation-patterns.md) <br>
- [Evidence Model](references/evidence-model.md) <br>
- [Report Template](references/report-template.md) <br>
- [Tribunal](references/tribunal.md) <br>
- [Verdict Rubric](references/verdict-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown audit report with verdict, evidence table, causal scan, side findings, and minimal next actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports mirror the user's language when invoked from non-English context and do not run code unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
