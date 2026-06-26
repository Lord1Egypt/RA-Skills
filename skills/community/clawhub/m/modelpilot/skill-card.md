## Description: <br>
Use this skill to test, compare, promote, replace, or clean up local Ollama models with repeatable two-round benchmarks, no-think verification, and local-only safety boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patmenciu](https://clawhub.ai/user/patmenciu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate installed local Ollama models against fixed fictional prompt sets before changing workflow model choices. It helps compare speed, format stability, no-think leakage, repeatability, and rollback readiness without relying on cloud APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark reports may store prompts and model responses locally. <br>
Mitigation: Use fictional or explicitly approved prompt files and review output paths before running benchmarks. <br>
Risk: Replacing or deleting a local model after weak evidence can disrupt an existing workflow. <br>
Mitigation: Require two benchmark rounds for replacement decisions, keep the previous model available for rollback, and approve any model download or deletion separately. <br>
Risk: No-think model names or settings may still produce reasoning traces or polluted structured output. <br>
Mitigation: Check generated output for thinking markers and avoid promotion into automated workflows when no-think or structured-output behavior is unstable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patmenciu/modelpilot) <br>
- [README](README.md) <br>
- [Example benchmark report](outputs/example_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, optional JSON benchmark inputs, and Markdown benchmark reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only Ollama workflow; benchmark reports may include prompts and model responses stored on the user's machine.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
