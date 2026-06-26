## Description: <br>
Audits HTTP security headers for user-specified websites, grades their posture A-F, and reports missing headers or server information leakage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to check websites they own or are authorized to test for common HTTP security headers, A-F posture grades, and obvious server information leakage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends HTTP requests to each user-specified target site, which may be visible to that site. <br>
Mitigation: Run it only against sites you own or are authorized to check. <br>
Risk: Header presence and grading are a narrow signal and may not represent the full security posture of a website. <br>
Mitigation: Use the results as triage guidance and confirm important findings with a broader security review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogue-agent1/headers) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text CLI report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports URL status, present and missing headers, severity labels, information-leak headers, score percentage, and A-F grade.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
