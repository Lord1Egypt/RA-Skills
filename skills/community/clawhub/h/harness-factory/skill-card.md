## Description: <br>
Use when building features, fixing complex bugs, or doing major refactoring by guiding an agent through a structured Plan, Build, Review, and Iterate workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guixiang123124](https://clawhub.ai/user/guixiang123124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan, delegate, review, and iterate on multi-file feature work, complex bug fixes, and major refactors with explicit sprint scope, mechanical checks, and review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes push, deployment, production verification, and optional automatic triggering steps that can affect release state without an explicit approval gate. <br>
Mitigation: Use a clean branch or isolated worktree, keep SPRINT.md file scope narrow, and require manual confirmation before git push, deployment, production verification, or AGENTS.md auto-trigger setup. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guixiang123124/harness-factory) <br>
- [Code Quality Checklist](references/code-quality-checklist.md) <br>
- [Evaluation Dimensions](references/evaluation-dimensions.md) <br>
- [Metrics](references/metrics.md) <br>
- [Security Checklist](references/security-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown workflow documents, inline shell commands, code changes, configuration snippets, and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can create SPRINT.md, REVIEW.md, BUILDER_REPORT.md, REVIEWER_REPORT.md, and HARNESS_REPORT.md files and can guide agent sessions through implementation and review.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
