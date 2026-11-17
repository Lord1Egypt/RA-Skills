## Description:

Send real-time alerts to NotiLens from any script, app, or AI agent for task lifecycle events, errors, completions, and metric tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notilens](https://clawhub.ai/user/notilens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this plugin to send task and application alerts, status updates, errors, output events, and operational metadata to NotiLens during automated workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alert messages, URLs, tags, and metadata are sent outside the local environment to NotiLens.

Mitigation: Only include data that is intended for NotiLens, and avoid sending tokens, private prompts, customer data, or sensitive error details.

Risk: The plugin requires NotiLens token and secret environment variables to send events.

Mitigation: Store NOTILENS_TOKEN and NOTILENS_SECRET as environment secrets and avoid placing them in messages, metadata, source files, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/notilens/skills/notilens-clawhub-plugin)
- [NotiLens homepage](https://www.notilens.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Configuration]

**Output Format:** [JavaScript function calls that send JSON webhook payloads and return the NotiLens API response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOTILENS_TOKEN and NOTILENS_SECRET environment variables.]

## Skill Version(s):

0.2.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
