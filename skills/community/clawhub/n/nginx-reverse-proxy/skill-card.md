## Description: <br>
Configures an nginx reverse proxy to bind a domain to a specified IP:port target. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudswave](https://clawhub.ai/user/cloudswave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server administrators use this skill to draft nginx reverse proxy configuration and supporting commands for routing a domain to a backend service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose sudo commands that write nginx configuration, reload nginx, or run certbot on a host. <br>
Mitigation: Review every command before execution, back up current nginx configuration, inspect the generated config, run nginx -t, and approve reload or certificate issuance manually. <br>
Risk: Incorrect domain or target IP:port values can route traffic to the wrong service. <br>
Mitigation: Verify the domain, DNS state, and target IP:port before writing configuration or requesting certificates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudswave/nginx-reverse-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with nginx configuration and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates nginx server block examples and administrative commands for the requested domain and target.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
