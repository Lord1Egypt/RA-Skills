## Description: <br>
Initialize and configure Traefik reverse proxy with Docker. Install Traefik, configure Docker Compose, set up service routing via path prefix or host-based routing, enable features like dashboard metrics logging tracing, configure Dashboard access via nip.io or path prefix <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[le-shi](https://clawhub.ai/user/le-shi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to set up a Traefik v3 reverse proxy with Docker Compose, configure service routing, and enable operational features such as dashboard access, logs, metrics, and tracing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default templates can expose an unauthenticated Traefik dashboard/API on a running reverse proxy. <br>
Mitigation: Review before installing or copying the templates, remove insecure dashboard/API exposure, protect access with authentication and preferably HTTPS, and restrict access by IP, VPN, or localhost. <br>
Risk: The Traefik container runs with Docker socket visibility. <br>
Mitigation: Use only on trusted private networks and review the Docker socket mount before deployment. <br>


## Reference(s): <br>
- [Features](references/features.md) <br>
- [Examples](references/examples.md) <br>
- [Summary](references/summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker Compose and Traefik dynamic configuration templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
