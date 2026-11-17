## Description:

Download videos from m3u8/HLS streams, Bilibili, and direct URLs using a running MediaGo instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caorushizi](https://clawhub.ai/user/caorushizi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to configure access to a MediaGo service, create video download tasks, monitor progress, and report download results in English or Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured MediaGo endpoint and optional API key may expose local service access or credential data if the endpoint or config file is not trusted.

Mitigation: Prefer localhost, avoid storing an API key unless needed, and protect or remove ~/.mediago-skill.json when the skill is no longer in use.

Risk: The skill constructs curl-based HTTP requests from user-provided URLs, names, and API keys; unsafe construction could mishandle crafted input.

Mitigation: Review generated commands before execution and use only trusted URLs, names, API keys, and MediaGo endpoints.

## Reference(s):

- [MediaGo ClawHub skill page](https://clawhub.ai/caorushizi/skills/mediago)
- [MediaGo project homepage](https://github.com/caorushizi/mediago)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update ~/.mediago-skill.json and call a configured MediaGo HTTP endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
