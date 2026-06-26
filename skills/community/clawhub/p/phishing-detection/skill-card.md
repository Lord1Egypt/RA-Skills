## Description: <br>
Analyzes URLs using heuristic algorithms to detect and identify phishing threats in real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, developers, and automation systems use this skill to submit URLs for phishing-risk analysis and receive a structured threat assessment for triage or workflow integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs are sent to an external third-party phishing-analysis service. <br>
Mitigation: Avoid submitting sensitive internal URLs, password reset links, credential-bearing query strings, tracking links, or confidential incident-response targets unless the provider's privacy and retention practices are acceptable. <br>
Risk: Heuristic phishing analysis can produce false positives or false negatives. <br>
Mitigation: Use the returned risk score and threat indicators as one signal in security triage, with human review or additional tooling for high-impact decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/phishing-detection) <br>
- [Phishing Detection API Docs](https://api.mkkpro.com:8005/docs) <br>
- [Phishing Detection API Route](https://api.mkkpro.com/security/phishing-detection) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, analysis, guidance] <br>
**Output Format:** [JSON threat assessment with phishing status, risk score, threat indicators, confidence, and timestamp] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a single URL string up to 2048 characters and returns a per-URL assessment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
