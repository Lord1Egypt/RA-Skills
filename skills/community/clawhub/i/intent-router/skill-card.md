## Description: <br>
Classify text into custom intents with confidence scoring and entity extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Daisuke134](https://clawhub.ai/user/Daisuke134) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to route user messages, classify NLU intents, and extract entities for multi-agent orchestration or text-classification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided text to a hosted classifier endpoint. <br>
Mitigation: Avoid sending secrets, credentials, regulated data, or confidential conversations unless the service's privacy practices are acceptable. <br>
Risk: Each request is a paid x402 call. <br>
Mitigation: Use spending limits, manual review, or operational controls before routing high-volume traffic through the skill. <br>
Risk: Intent classification can be incorrect or low confidence. <br>
Mitigation: Review confidence scores and add fallback handling for uncertain or business-critical routing decisions. <br>


## Reference(s): <br>
- [intent-router skill page](https://clawhub.ai/Daisuke134/intent-router) <br>
- [intent-router hosted endpoint](https://anicca-proxy-production.up.railway.app/api/x402/intent-router) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces intent matches, confidence scores, optional secondary intent data, extracted entities, and detected language.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
