## Description: <br>
Debug prompts that produce unexpected AI outputs by diagnosing failure modes, identifying ambiguity and conflicting instructions, testing variations, comparing model responses, and improving prompt quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt authors, and agent builders use this skill to diagnose prompts that produce unexpected outputs, compare prompt variations, detect prompt anti-patterns, score prompt quality, and produce improved prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rewritten prompts may introduce incorrect, misleading, or overly broad instructions if accepted without review. <br>
Mitigation: Review and test rewritten prompts before using them as production system or agent instructions. <br>
Risk: Prompt debugging often requires sharing the original prompt, which may contain secrets or confidential information. <br>
Mitigation: Remove secrets and confidential data before using the skill unless that information can be exposed to the active AI session. <br>
Risk: Static prompt analysis may not predict every model-specific behavior. <br>
Mitigation: Validate proposed prompt changes with the intended model, data, and use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/prompt-debugger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Text, Markdown, or JSON diagnostic reports with prompt rewrites, variation comparisons, quality scores, and anti-pattern findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute prompts; analysis is static and should be tested with the target model and use case.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
