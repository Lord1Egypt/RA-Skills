## Description: <br>
Multi User Privacy helps OpenClaw and ClawHub operators isolate user memory, route per-user sessions, check sensitive content, enforce quotas, and administer multi-user agent deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lz84](https://clawhub.ai/user/lz84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to add privacy controls to multi-user OpenClaw deployments: per-user memory isolation, role-aware sensitive-content checks, session and subagent routing, quota management, monitoring, and a web administration surface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence identifies this as a broad multi-user administrative control-plane skill with hard-coded administrator and recipient identifiers. <br>
Mitigation: Replace all hard-coded administrator and recipient identifiers with deployment-specific values before installation, and review post-install file changes. <br>
Risk: The security evidence states that powerful web administration controls are exposed without authentication. <br>
Mitigation: Add authentication and bind the web administration server to localhost or another restricted interface before use. <br>
Risk: The security guidance warns that real-looking secrets may appear in documentation or configuration examples. <br>
Mitigation: Rotate or remove any real-looking secrets and identifiers found in docs, templates, or generated local state before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lz84/multi-user-privacy) <br>
- [Publisher Profile](https://clawhub.ai/user/lz84) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, JavaScript and Python modules, shell commands, JSON/YAML configuration, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes administrative scripts and services that may read or write local OpenClaw skill, memory, quota, routing, monitoring, and web-admin files.] <br>

## Skill Version(s): <br>
0.9.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
