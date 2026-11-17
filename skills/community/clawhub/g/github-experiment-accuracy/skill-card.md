## Description:

Given a GitHub repository URL and a data file, this skill guides an agent through running the project, validating prediction accuracy, and producing workflow and accuracy reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinyyc](https://clawhub.ai/user/kevinyyc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess a GitHub project's predictive accuracy against a supplied dataset and generate experiment results for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may load models from arbitrary repositories using unsafe PyTorch deserialization, which can execute untrusted code.

Mitigation: Use only trusted and verified repositories, commits, and model artifacts in a disposable sandbox with no secrets or sensitive files; prefer safe model formats or weights-only loading.

## Reference(s):

- [Workflow Reference](references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/kevinyyc/skills/github-experiment-accuracy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Markdown, Configuration]

**Output Format:** [Markdown guidance with inline shell, PowerShell, and Python snippets; generated reports may be Markdown or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces experiment reports and daily result files such as accuracy_report.md, experiment_report.md, and outputs/daily_results.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
