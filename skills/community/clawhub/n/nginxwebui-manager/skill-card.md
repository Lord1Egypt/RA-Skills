## Description:

Manage NginxWebUI reverse proxy rules via its REST API. List/create/delete servers and locations, reload nginx, manage upstreams. All calls through docker exec into the nginxwebui container.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaixi](https://clawhub.ai/user/zaixi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to inspect and manage NginxWebUI reverse proxy servers, locations, upstreams, and nginx reload/check operations from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful NginxWebUI credentials and can make live proxy configuration changes.

Mitigation: Install and run it only in a tightly controlled workspace with trusted local users, and confirm delete or reload actions outside the skill before applying them.

Risk: The skill can persist the NginxWebUI admin token in a shared .env file.

Mitigation: Avoid shared credential files where possible and rotate NginxWebUI credentials after testing or other temporary use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker access, NginxWebUI admin credentials, and a running nginxwebui container.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
