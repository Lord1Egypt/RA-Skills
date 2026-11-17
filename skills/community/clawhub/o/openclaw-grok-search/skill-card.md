## Description:

Openclaw Grok Search provides cross-platform real-time web research through an OpenAI-compatible Grok endpoint and returns structured JSON with content, sources, and raw response data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxunjinmu](https://clawhub.ai/user/moxunjinmu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to perform time-sensitive web research, verify versions and documentation, troubleshoot issues with source-backed results, and obtain structured JSON output from a configured Grok-compatible endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a non-placeholder API key in config.json.

Mitigation: Remove artifact/config.json or replace it with a private local configuration, and rotate any exposed key before use.

Risk: The default configuration sends requests through a third-party proxy endpoint.

Mitigation: Verify that the endpoint is trusted before use and prefer an explicitly configured endpoint controlled by the user or organization.

Risk: Search queries and related context are sent to the configured external endpoint.

Mitigation: Avoid sending secrets, private code, personal data, credentials, or internal URLs as search queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moxunjinmu/skills/openclaw-grok-search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON object with ok, content, sources, raw, and request metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs, usage metadata, elapsed time, and error details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
