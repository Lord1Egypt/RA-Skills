## Description: <br>
Orchestrates multi-domain review across code, architecture, tests, and security in a single pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill before merging major feature branches or broad changes to coordinate code, architecture, test, security, and quality reviews into one consolidated action plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review workflow may automatically persist backlog findings through a local deferred-capture command. <br>
Mitigation: Review or disable the deferred-capture step before use on private, regulated, or security-sensitive code, and confirm where any backlog data is stored. <br>
Risk: Broad review-related prompts may activate multi-domain review and dispatch multiple review agents. <br>
Mitigation: Confirm the intended review scope, selected review mode, and agent set before relying on results or applying follow-up changes. <br>
Risk: Integrated review output can combine findings from multiple reviewers before each finding is independently verified. <br>
Mitigation: Require evidence-linked findings and human verification before changing code or promoting recommendations into release blockers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-unified-review) <br>
- [Pensive plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>
- [Review workflow core](modules/review-workflow-core.md) <br>
- [Output format templates](modules/output-format-templates.md) <br>
- [Quality checklist patterns](modules/quality-checklist-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with an executive summary, findings, action items, and evidence appendix; may include shell commands for deferred finding capture.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Integrates selected domain-review results into prioritized recommendations and backlog capture guidance.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
