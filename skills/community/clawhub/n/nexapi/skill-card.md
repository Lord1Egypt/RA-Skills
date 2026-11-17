## Description:

NexAPI tool API invocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avrinbai](https://clawhub.ai/user/avrinbai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to discover NexAPI utility endpoints, configure API access, cache endpoint metadata, and call selected tool, data, content, or operations APIs with compact output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a NexAPI API key in plaintext and send it to a configurable, undocumented endpoint.

Mitigation: Install only if the NexAPI service and runtime environment are trusted; avoid setting NEXAPI_BASE_URL unless the destination is fully trusted, prefer environment-based API keys over local plaintext storage on shared systems, and check generated config file permissions after using auth set.

## Reference(s):

- [NexAPI service endpoint](https://api.avrinbai.cn)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default command output is compact; --verbose requests the full API response, and binary responses return metadata instead of raw bytes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
