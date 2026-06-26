## Description: <br>
Run a local security audit on an OpenClaw environment and summarize risks, impacted locations, and prioritized remediation steps without exposing raw secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haooyi](https://clawhub.ai/user/haooyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit a local OpenClaw installation or workspace for leaked secrets, risky configuration, exposed services, and file or host security issues. It produces prioritized findings and remediation guidance for local review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit reports can contain sensitive host, workspace, file path, process, listener, and masked secret evidence. <br>
Mitigation: Keep generated reports private, review them before sharing, and run the skill only when intentionally auditing the local machine or OpenClaw workspace. <br>
Risk: The skill performs local host, network, configuration, filesystem, git, and secret scanning. <br>
Mitigation: Run it in the intended local environment and use provided options such as --no-host or --no-git when those checks are not appropriate. <br>


## Reference(s): <br>
- [Openclaw Security Audit ClawHub page](https://clawhub.ai/haooyi/openclaw-sec-audit) <br>
- [haooyi publisher profile](https://clawhub.ai/user/haooyi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Console summary plus optional text, JSON, and Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include local usernames, hostnames, file paths, process or listener details, security posture information, and masked secret examples.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
