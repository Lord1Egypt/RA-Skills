## Description: <br>
Jury Review creates a dynamic, role-based review panel for multidimensional scoring, extreme-case challenges, and iterative improvement of code or technical tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuxNd](https://clawhub.ai/user/kukuxNd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to assemble a task-specific review panel, score work across dimensions such as security, performance, testing, architecture, and documentation, and guide iterative improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may activate for broad review or quality-assessment requests. <br>
Mitigation: Use it intentionally for review tasks and keep the review scope explicit. <br>
Risk: The optional scorer reads a file path supplied at runtime. <br>
Mitigation: Run the scorer only against files you intentionally want reviewed. <br>
Risk: Role-based scoring and extreme challenge feedback can overemphasize edge cases or produce subjective guidance. <br>
Mitigation: Treat the feedback as review support and verify recommendations before applying changes. <br>


## Reference(s): <br>
- [Jury scoring guide](references/scoring-guide.md) <br>
- [AutoResearch](https://github.com/karpathy/autoresearch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown review plans and feedback, with optional JSON scoring output from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the user to choose additional challenge reviewers before producing final review feedback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
