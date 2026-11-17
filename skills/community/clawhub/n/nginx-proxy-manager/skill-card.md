## Description:

Manage Nginx Proxy Manager (NPM) for reverse proxy and SSL termination to internal services like staging/prod apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mw-slc](https://clawhub.ai/user/mw-slc)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure Nginx Proxy Manager reverse proxy hosts, SSL certificates, HTTPS redirects, websocket support, and domain routing for internal staging or production services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials or tokens could be exposed if supplied directly in prompts or hardcoded into shared skill content.

Mitigation: Provide NPM credentials through environment variables or a local secret store, and review shared copies for real domains, IPs, emails, and tokens.

Risk: Incorrect production proxy or SSL changes could disrupt application traffic.

Mitigation: Review production changes before applying them, document or export previous values, and apply changes to staging first when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mw-slc/skills/nginx-proxy-manager)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checklist-style operational guidance for Nginx Proxy Manager changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
