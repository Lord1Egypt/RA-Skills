## Description: <br>
Manage ISPConfig servers: automated site provisioning, domains, mailboxes, DNS, databases, SSL, backups, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homeofe](https://clawhub.ai/user/homeofe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server administrators use this skill to let an agent manage ISPConfig hosting resources, including sites, DNS, mail, databases, SSL, backups, and one-command provisioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live control over ISPConfig, including destructive and VM-level actions. <br>
Mitigation: Install only when agent-based ISPConfig administration is intended, and require human approval for deletes, password changes, server or system configuration edits, permission changes, and OpenVZ operations. <br>
Risk: Default write access may be broader than necessary for routine administration. <br>
Mitigation: Use a least-privilege ISPConfig remote user and start with readOnly=true or a tight allowedOperations whitelist. <br>
Risk: Misconfigured credentials or TLS settings can expose administrative access to the target server. <br>
Mitigation: Store the ISPConfig password as a secret, keep verifySsl enabled unless explicitly required, and limit network access to the intended ISPConfig endpoint. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/homeofe/openclaw-ispconfig) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [JSON and text returned by OpenClaw tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live ISPConfig API actions when configured with server credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, README, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
