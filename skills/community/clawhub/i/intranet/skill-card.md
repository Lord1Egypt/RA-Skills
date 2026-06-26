## Description: <br>
Lightweight local HTTP file server with plugin support. Serves static files from a webroot, mounts plugin directories at URL prefixes via config, and runs index.py entry points as CGI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to start and manage a lightweight local HTTP server for workspace files, plugin-mounted directories, and optional CGI-backed local pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional CGI support can execute plugin code more broadly than the documentation describes. <br>
Mitigation: Keep CGI disabled for untrusted content, review every mounted plugin directory before use, and do not rely on plugin hash settings as the only protection. <br>
Risk: Exposing the server beyond localhost can make workspace files and intranet pages reachable to other clients. <br>
Mitigation: Keep the default localhost bind unless remote access is required; when binding to a network interface, enable token authentication and an allowed-hosts list. <br>
Risk: Configuration and runtime files may contain tokens or access settings. <br>
Mitigation: Treat workspace/intranet/config.json and workspace/intranet/.conf as sensitive files and avoid serving, logging, or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/intranet) <br>
- [Setup guide](artifact/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and writes local server state under the workspace intranet directory.] <br>

## Skill Version(s): <br>
3.2.7 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
