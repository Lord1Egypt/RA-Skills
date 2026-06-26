## Description: <br>
Security partner for Inner Warden - validates commands before execution, monitors server health, diagnoses and fixes issues. Requires Inner Warden installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maiconburn](https://clawhub.ai/user/maiconburn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server operators use this skill to work with Inner Warden for security status checks, command validation, service health diagnostics, and approved remediation on Linux or Darwin hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose sudo-level service, log, configuration, and disk-maintenance commands on a server. <br>
Mitigation: Install only when you use or plan to use Inner Warden, review proposed commands, and approve privileged remediation only when it matches your maintenance intent. <br>
Risk: Dashboard authentication may require the user to provide the local Inner Warden dashboard password to the agent session. <br>
Mitigation: Provide the dashboard password only when you intend the local agent to authenticate to the localhost API; otherwise use CLI-only workflows or disable dashboard auth. <br>
Risk: Initial setup relies on downloading and running an install script and release binaries. <br>
Mitigation: Download and inspect the install script before execution, and verify installed binaries against their SHA256 sidecar files. <br>


## Reference(s): <br>
- [Inner Warden website](https://innerwarden.com) <br>
- [Inner Warden GitHub project](https://github.com/InnerWarden/innerwarden) <br>
- [Inner Warden releases](https://github.com/InnerWarden/innerwarden/releases) <br>
- [Inner Warden issue tracker](https://github.com/InnerWarden/innerwarden/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Inner Warden or its localhost API for full operation; privileged changes are proposed for user approval before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
