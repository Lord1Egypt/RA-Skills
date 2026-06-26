## Description: <br>
Verify model identity by testing 4 dimensions: knowledge cutoff, safety style, multimodal capability, and thinking language patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[civen-cn](https://clawhub.ai/user/civen-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, evaluators, and agent users use this skill to run informal checks when they need to verify a model claim or investigate suspicious model behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The verification result is informal and may be mistaken for proof of model identity. <br>
Mitigation: Use the output as a screening aid only, and confirm security-critical model identity with official provider metadata, platform controls, or signed deployment configuration. <br>
Risk: The phishing-prevention prompt could drift from defensive review into unsafe technique generation. <br>
Mitigation: Keep the test framed around prevention and defensive measures, and avoid requests for operational misuse details. <br>
Risk: Reasoning-model checks can encourage requests for hidden reasoning. <br>
Mitigation: Evaluate visible answer style and allowed summaries without asking the model to reveal private chain-of-thought. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown table with pass/fail results, notes, a verdict, and suspicious points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records the actual questions and answers used as evidence for each check.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
