## Description: <br>
Explore nginx-proxied directories to discover tools and utilities, read README.md files for usage details, and help identify executable projects from a configured nginx URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaojun0](https://clawhub.ai/user/shaojun0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect a trusted nginx-served directory tree, read tool documentation, and decide which hosted utilities may help with a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to download, change permissions on, install dependencies for, or execute remotely hosted tools. <br>
Mitigation: Require explicit user approval for each download, chmod, dependency installation, and execution step. <br>
Risk: A compromised or uncontrolled nginx server could provide malicious or misleading tools and README instructions. <br>
Mitigation: Use only tightly controlled trusted nginx servers, verify checksums or signatures where possible, and review downloaded files before use. <br>
Risk: Skipping SSL verification can weaken transport security on networks that are not fully trusted. <br>
Mitigation: Keep SSL verification enabled where possible and limit skip-verify behavior to controlled internal environments with self-signed certificates. <br>
Risk: Downloaded tools may affect the host environment when executed directly. <br>
Mitigation: Run downloaded tools in an isolated sandbox and clean up temporary files after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaojun0/nginx-explorer) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured NGINX_URL and uses curl to inspect nginx-served directory listings and README files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
