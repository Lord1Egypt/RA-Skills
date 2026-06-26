## Description: <br>
Mini PIV is a lightweight, discovery-driven feature builder that asks a few questions, generates a PRP, executes implementation, and validates changes for small-to-medium features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SmokeAlot420](https://clawhub.ai/user/SmokeAlot420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to turn a small or medium feature request into a PRP-backed implementation flow with codebase analysis, execution, validation, debugging, and commit steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can stage and commit all repository changes. <br>
Mitigation: Run it from a clean working tree, keep secrets and unrelated untracked files out of the repository, and review the generated PRP and final diff before allowing the commit step. <br>
Risk: Generated implementation guidance or code changes may be incorrect for the target project. <br>
Mitigation: Use the built-in validation loop, independently review test results and diffs, and request human guidance when validation reports HUMAN_NEEDED or repeated gaps. <br>


## Reference(s): <br>
- [Mini PIV ClawHub Page](https://clawhub.ai/SmokeAlot420/mini-piv) <br>
- [FTW Homepage](https://github.com/SmokeAlot420/ftw) <br>
- [Codebase Analysis for Feature Planning](references/codebase-analysis.md) <br>
- [Create BASE PRP](references/generate-prp.md) <br>
- [Execute BASE PRP](references/execute-prp.md) <br>
- [PIV Executor Agent](references/piv-executor.md) <br>
- [PIV Validator Agent](references/piv-validator.md) <br>
- [PIV Debugger Agent](references/piv-debugger.md) <br>
- [Base PRP Template](assets/prp_base.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create PRP and analysis Markdown files, modify repository code, run validation commands, and stage and commit changes when the workflow completes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
