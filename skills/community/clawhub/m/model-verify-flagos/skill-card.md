## Description: <br>
Verifies a user-specified target model by running the serving stack with and without FlagGems/FlagCX, then diffs the results to isolate model-specific or multi-chip stack failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to verify whether a target model can run on a containerized serving stack and whether failures come from the base model path or the multi-chip operator and communication stack. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote model IDs may execute code because the workflow enables remote-code execution by default. <br>
Mitigation: Run the skill only in an isolated, disposable container and use trusted, vetted model repositories or local model paths. <br>


## Reference(s): <br>
- [Multi-Chip Error Classification](artifact/references/multichip-errors.md) <br>
- [ClawHub release page](https://clawhub.ai/wbavon/model-verify-flagos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with bash commands and a structured JSON verification report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report compares base-stack and full multi-chip runs and includes a recommended stack value of full, base, or none.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
