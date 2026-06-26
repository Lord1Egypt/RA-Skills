## Description: <br>
Creates a standard Nginx/OpenResty reverse proxy config file for a service and reloads the web server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieyuanqing](https://clawhub.ai/user/xieyuanqing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to generate an Nginx/OpenResty reverse proxy configuration for a service and reload a Dockerized web server after testing the generated config. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite or delete live Nginx configuration files and reload a Dockerized web server. <br>
Mitigation: Use a known-safe config directory and container name, back up existing configs first, and review changes before running against a live server. <br>
Risk: Weak input checks can make untrusted service names, domains, ports, paths, or container names unsafe. <br>
Mitigation: Only pass trusted, expected values for service names, domains, ports, paths, and container names. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xieyuanqing/nginx-config-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Shell commands, Text] <br>
**Output Format:** [Nginx configuration file plus shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and docker; writes to the configured Nginx conf.d directory and reloads the specified container.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
