## Description: <br>
Multi-user workspace management with sandbox permissions, user profiles, and relationship networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shun-dong](https://clawhub.ai/user/shun-dong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace administrators use this skill to configure multi-user OpenClaw workspaces with per-user profiles, relationship-aware information sharing, and role-based sandbox settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User profile and relationship files can contain private data. <br>
Mitigation: Treat FRIENDS/ and RELATIONS/ as private data and share information only when explicitly permitted by RELATIONS/. <br>
Risk: Malformed or spoofed user IDs could select the wrong profile or relationship file. <br>
Mitigation: Validate userId with a strict lowercase letters, numbers, underscores, and hyphens pattern, and match it to USER.md before reading files. <br>
Risk: Untrusted users with unsandboxed administrator sessions may access broader workspace data. <br>
Mitigation: Reserve unsandboxed administrator sessions for trusted users and keep guest sessions in isolated, periodically cleaned directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shun-dong/multi-user-workspace) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON5 and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
