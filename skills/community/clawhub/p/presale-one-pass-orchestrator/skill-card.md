## Description: <br>
Run or supervise a one-pass Codex implementation with preflight gates, stepwise plan execution, and strict QA defect loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DTsiomo](https://clawhub.ai/user/DTsiomo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and delivery engineers use this skill to execute an approved presale implementation plan in one controlled pass, with preflight gates, step-by-step verification, and a mandatory defect loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may modify project files and run check commands while carrying out an approved plan. <br>
Mitigation: Install only for trusted repositories and review the plan plus verification commands before execution. <br>
Risk: Incomplete readiness checks or out-of-scope plan content can lead to unintended implementation work. <br>
Mitigation: Require explicit readiness approval, no open review comments, and scope-locked plan execution before proceeding. <br>


## Reference(s): <br>
- [QA Defect Loop](references/qa-defect-loop.md) <br>
- [ClawHub Release Page](https://clawhub.ai/DTsiomo/presale-one-pass-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with command snippets and file-change details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes verification status, defects found and fixed, risks, debts, open questions, and reproducible check commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
