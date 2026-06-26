## Description: <br>
KU Portal helps an OpenClaw agent query Korea University KUPID portal, library, timetable, course, scholarship, notice, cafeteria, and Canvas LMS information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garibong-labs](https://clawhub.ai/user/garibong-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Korea University users use this skill to retrieve campus portal, library, timetable, course, notice, scholarship, cafeteria, and LMS information from a local CLI. Login-only commands require user-provided KUPID credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive KUPID username and password data for login-only portal and LMS commands. <br>
Mitigation: Install only when the publisher and dependency are trusted, keep ~/.config/ku-portal/credentials.json chmod 600, and delete credential files when uninstalling. <br>
Risk: Portal and LMS session data is stored in local cache files. <br>
Mitigation: Avoid sharing ~/.cache/ku-portal-mcp and remove cached session files when access is no longer needed. <br>
Risk: The setup script installs or upgrades the ku-portal-mcp dependency, which can change runtime behavior. <br>
Mitigation: Pin the dependency version for reproducible deployments when operational stability is required. <br>


## Reference(s): <br>
- [KU Portal ClawHub page](https://clawhub.ai/garibong-labs/ku-portal) <br>
- [ku-portal-mcp upstream project](https://github.com/SonAIengine/ku-portal-mcp) <br>
- [garibong-labs ku-portal-mcp fork](https://github.com/garibong-labs/ku-portal-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [CLI text output with optional JSON credential configuration and ICS timetable file export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the ku-portal-mcp dependency; login-only commands read credentials from ~/.config/ku-portal/credentials.json and may use session cache files under ~/.cache/ku-portal-mcp.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
