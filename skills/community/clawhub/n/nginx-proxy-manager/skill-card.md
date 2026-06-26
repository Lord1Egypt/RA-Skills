## Description: <br>
Manage Nginx Proxy Manager (NPM) for reverse proxy and SSL termination to internal services like staging/prod apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mw-slc](https://clawhub.ai/user/mw-slc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure Nginx Proxy Manager proxy hosts, SSL certificates, HTTPS settings, websocket support, and routing for staging or production services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NPM admin credentials may be exposed or mishandled. <br>
Mitigation: Store credentials outside the skill, use environment variables or a local secret store, and avoid logging or publishing real tokens. <br>
Risk: Proxy, DNS, upstream, or SSL changes can affect production traffic. <br>
Mitigation: Confirm the domain, DNS target, upstream host and port, and SSL options before applying changes; export or document existing production settings first. <br>
Risk: HSTS or HTTPS redirect changes can cause redirect loops or hard-to-reverse browser behavior. <br>
Mitigation: Validate routing and certificates first, apply changes to staging when possible, and enable HSTS only after validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mw-slc/nginx-proxy-manager) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for domains, hosts, credentials, and upstream services.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
