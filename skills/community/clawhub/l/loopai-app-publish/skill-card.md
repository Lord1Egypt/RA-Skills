## Description:

Publishes AI application, software, or tool listings to App Hub with app metadata, screenshots, author details, pricing, communities, and URL reachability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeamchen](https://clawhub.ai/user/jeamchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app creators use this skill to create, update, validate, and inspect App Hub listings for AI apps, software, and tools before publishing them to a showcase center.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace App Hub credentials can be exposed through verbose logging.

Mitigation: Avoid verbose mode until token redaction is fixed, keep logs access-controlled, and use narrowly scoped App Hub tokens.

Risk: A custom API base URL can receive the App Hub token.

Mitigation: Use only trusted HTTPS App Hub API origins and avoid custom API URLs unless they have been reviewed.

Risk: App URL validation performs outbound network requests from the agent environment.

Mitigation: Treat validation as egress from the agent workspace and validate only URLs that are expected and safe to contact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeamchen/skills/loopai-app-publish)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read an App Hub token from the workspace and may make outbound HTTP requests to validate app URLs and call App Hub APIs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
