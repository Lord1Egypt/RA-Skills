## Description: <br>
Detect prompt injection attacks in text. Returns risk score and detected patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Promptguard to scan untrusted text for common prompt-injection patterns before passing it to AI agents or downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local FastAPI service is unauthenticated if exposed beyond local use. <br>
Mitigation: Run it locally or add access controls before exposing it to public networks. <br>
Risk: Pattern matching can miss novel prompt-injection attempts or flag benign text. <br>
Mitigation: Use the score and detected patterns as one signal in a broader review policy. <br>


## Reference(s): <br>
- [Promptguard on ClawHub](https://clawhub.ai/mirni/promptguard) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API response] <br>
**Output Format:** [JSON object with risk_score, patterns_detected, and input_length fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scans one text string per request, with input constrained to 1-100,000 characters.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
