## Description: <br>
Performs a quick local host readiness check and reports basic disk, CPU, memory, process, and service status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankou11](https://clawhub.ai/user/ankou11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to get a quick local readiness snapshot before investigating host or OpenClaw service issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health-check output may expose process, service, and host capacity details. <br>
Mitigation: Keep results local and redact host-specific details before sharing output outside the operating team. <br>
Risk: A clean local snapshot may be mistaken for proof that OpenClaw is fully current or hardened. <br>
Mitigation: Treat the output as basic diagnostics and pair it with environment-specific security review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ankou11/healthcheck-ready) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text status output from local shell checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local host metrics and service presence; does not perform remediation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
