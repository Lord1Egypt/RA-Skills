## Description: <br>
PIV - Plan Implement Validate orchestrates multi-phase software development by creating PRDs and PRPs, coordinating implementation sub-agents, and validating changes through iterative Plan, Implement, Validate loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SmokeAlot420](https://clawhub.ai/user/SmokeAlot420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and deliver multi-phase software changes with PRDs, PRPs, codebase analysis, sub-agent execution, validation reports, debugging retries, workflow tracking, and commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify repositories, run project-defined commands, spawn sub-agents, and create git commits. <br>
Mitigation: Use it in a version-controlled or disposable project, inspect generated plans and diffs, and require explicit approval before file overwrites, arbitrary validation commands, or commits. <br>
Risk: Generated PRPs, implementation summaries, and validation reports can be incomplete or misleading. <br>
Mitigation: Review generated PRPs before execution and rely on independent validation reports before accepting or committing changes. <br>


## Reference(s): <br>
- [Codebase Analysis for Feature Planning](artifact/references/codebase-analysis.md) <br>
- [Create PRD](artifact/references/create-prd.md) <br>
- [Create BASE PRP](artifact/references/generate-prp.md) <br>
- [Execute BASE PRP](artifact/references/execute-prp.md) <br>
- [PIV Executor Agent](artifact/references/piv-executor.md) <br>
- [PIV Validator Agent](artifact/references/piv-validator.md) <br>
- [PIV Debugger Agent](artifact/references/piv-debugger.md) <br>
- [Project homepage](https://github.com/SmokeAlot420/ftw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update PRD, PRP, workflow, source, test, and commit artifacts during the workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
