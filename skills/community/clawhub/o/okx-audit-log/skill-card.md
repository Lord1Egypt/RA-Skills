## Description: <br>
Provides the OKX Onchain OS audit log path, JSON Lines format, entry fields, and rotation behavior without reading or displaying log contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to tell users where the OKX Onchain OS audit log is stored and how it is structured for offline troubleshooting, while avoiding disclosure of the log contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit logs may contain sensitive command history or troubleshooting data. <br>
Mitigation: Provide only the log location and format; have users review or redact the file locally before sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/okx-audit-log) <br>
- [OKX Web3 Homepage](https://web3.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown response with a file path and structured log-format details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not read or display audit log contents.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
