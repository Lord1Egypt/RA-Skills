## Description:

Home Assistant custom integration patterns and architectural decisions. Use when building HACS integrations, custom components, or API bridges for Home Assistant. Covers service response data, HTTP views, storage APIs, and integration architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usimic](https://clawhub.ai/user/usimic)

### License/Terms of Use:


## Use Case:

Developers building Home Assistant custom integrations, HACS components, or API bridges use this skill to choose patterns for service responses, HTTP views, storage, integration structure, and testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Home Assistant API behavior can change across target versions.

Mitigation: Verify the guidance against the target Home Assistant version and review breaking changes before implementation.

Risk: Example integration patterns may be applied without sufficient review.

Mitigation: Review generated code or configuration, require authentication for HTTP views, and test service responses, storage persistence, and config flows before deployment.

## Reference(s):

- [Home Assistant integration basics](https://developers.home-assistant.io/docs/creating_integration_index)
- [Home Assistant service calls](https://developers.home-assistant.io/docs/dev_101_services)
- [Home Assistant HTTP views](https://developers.home-assistant.io/docs/api/webserver)
- [Home Assistant blog](https://www.home-assistant.io/blog/)
- [HACS publishing guidelines](https://hacs.xyz/docs/publish/start)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides patterns, version notes, and a testing checklist for Home Assistant integration work.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
