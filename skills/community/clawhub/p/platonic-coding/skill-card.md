## Description: <br>
Intelligent orchestrator for Platonic Coding workflow. Auto-detects project state and routes to the right next step: initialize a project, run the recovery flow for existing code, formalize drafts into RFCs, refine specs, implement from guides with tests, or review code compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caesar0301](https://clawhub.ai/user/caesar0301) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a specification-driven development workflow: scaffold or recover project specs, refine RFCs, create implementation guides, implement code and tests, and produce spec-compliance review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change specifications, implementation guides, code, and tests in a target repository. <br>
Mitigation: Use it only in repositories where that behavior is intended, review diffs before accepting changes, and prefer explicit operation names for scoped work. <br>
Risk: Skipping confirmation gates can allow the workflow to proceed without intermediate review. <br>
Mitigation: Avoid the 'no confirmations' mode unless the operator has already reviewed the implementation guide, coding plan, and expected repository changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/caesar0301/platonic-coding) <br>
- [Complete Reference](artifact/references/REFERENCE.md) <br>
- [Workflow Overview](artifact/references/WORKFLOW/workflow-overview.md) <br>
- [Full Implementation Workflow](artifact/references/IMPL/impl-full.md) <br>
- [Spec Compliance Review](artifact/references/REVIEW/review-spec-compliance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, source files, tests, configuration snippets, shell commands, and review reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project specs, implementation guides, code, tests, and report-only review artifacts depending on the selected operation.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
