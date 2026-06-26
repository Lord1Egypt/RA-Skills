## Description: <br>
Phy Session Audit is a zero-dependency session and cookie security auditor that scans common web framework source code for session management weaknesses mapped to OWASP A07:2021. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to run local static checks for session and cookie weaknesses, including missing cookie flags, tokens in URLs, session fixation, missing CSRF protection, weak session IDs, and broad cookie domains. It can also be used as a CI gate when teams want critical or high findings to fail a build. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Static pattern checks can produce false positives or miss framework-specific context. <br>
Mitigation: Review reported findings before remediation or release decisions, and treat the scanner as a focused aid rather than a complete application security assessment. <br>
Risk: CI mode can fail builds on reported critical or high findings. <br>
Mitigation: Enable --ci only after the team accepts the failure threshold, and use severity filtering when a narrower gate is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PHY041/phy-session-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and YAML examples; scanner reports are plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CI mode exits non-zero when critical or high findings are reported.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
