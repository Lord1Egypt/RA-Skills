## Description:

Service marketplace: publish data as services, consume hub services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangboheng](https://clawhub.ai/user/tangboheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to publish local data or capabilities as hub services and to discover, call, and combine services exposed by other agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service examples can expose local files.

Mitigation: Publish file-backed services only with path containment, explicit allowlists, authentication, and user approval.

Risk: API service examples can make arbitrary outbound requests.

Mitigation: Restrict URL-fetch services to approved destinations, enforce timeouts, and review request parameters before publication.

Risk: Hub and service keys may be mishandled.

Mitigation: Use the skill in a controlled environment, prefer wss:// for remote hubs, avoid logging keys, and set bounded key lifecycles.

Risk: Client code may be imported from mutable workspaces.

Mitigation: Pin and verify dependencies and avoid importing client code from untrusted or mutable workspace paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tangboheng/skills/hub-client)
- [Claw-Service-Hub Homepage](https://github.com/TangBoheng/Claw-Service-Hub)
- [wttr.in Weather API](https://wttr.in/{city}?format=j1)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include provider and consumer templates, service discovery and call flows, environment variables, dependency installation, troubleshooting, and optional key lifecycle guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
