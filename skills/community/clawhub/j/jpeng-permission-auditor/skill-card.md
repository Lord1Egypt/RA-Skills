## Description: <br>
Audit tool usage patterns and permissions to identify security risks and excessive access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit agent tool logs, compare required and granted permissions, and generate security reports with recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool logs and permission lists can contain sensitive operational details. <br>
Mitigation: Use logs you are comfortable processing locally and redact secrets or sensitive identifiers before audit. <br>
Risk: Static tool-risk mappings may not fully cover custom or newly introduced tools. <br>
Mitigation: Manually review unknown tool names and update the risk mapping before relying on the report for access decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jpengcheng523-netizen/jpeng-permission-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Guidance] <br>
**Output Format:** [JavaScript objects and plain-text CLI reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local tool logs and permission lists; server security evidence found no hidden access, network activity, persistence, or destructive behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
