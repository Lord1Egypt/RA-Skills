## Description: <br>
Deterministic rule-based system for classifying clarified input into a single primary task category and assigning execution complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omprasad122007-rgb](https://clawhub.ai/user/omprasad122007-rgb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to classify clarified user requests before task decomposition, route them to suitable handlers, and assign complexity, risk, and confidence signals for downstream planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Classification and audit logging can expose sensitive request content if the surrounding agent platform records raw inputs without suitable controls. <br>
Mitigation: Confirm platform logging, human-review queues, encryption, access controls, and retention policy before using the skill with sensitive requests. <br>
Risk: Incorrect classification can route a request to the wrong downstream workflow or hide uncertainty. <br>
Mitigation: Use the skill's low-confidence, high-risk, and ambiguity escalation paths for clarification or human review before execution planning. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/omprasad122007-rgb/input-classification-v1) <br>
- [Classification Models](references/classification-models.md) <br>
- [System Integration](references/system-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured ClassificationResult fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single primary category, up to three secondary tags, complexity level, risk level, confidence score, and routing state.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
