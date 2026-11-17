## Description:

Manage Lemonade Servers natively for system info, health status, model listing, model lifecycle actions, LLM chats, and stable-diffusion image generation on local or remote AI NPU/GPU clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-martinez](https://clawhub.ai/user/james-martinez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Lemonade Server health, manage model downloads and memory state, and send text or image generation requests to trusted local or remote servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API keys may be sent to local or remote Lemonade Server endpoints, including plain HTTP URLs.

Mitigation: Use trusted endpoints only, prefer localhost or HTTPS remote URLs, and avoid sending sensitive prompts to untrusted servers.

Risk: Model pull, load, and unload operations can change server state and consume disk, bandwidth, and accelerator memory.

Mitigation: Confirm the intended server and model before state-changing operations, check health and available resources first, and unload inactive models when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-martinez/skills/lemonade-server-manager)
- [Publisher profile](https://clawhub.ai/user/james-martinez)
- [Project homepage](https://github.com/james-martinez/lemonade-server-manager)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with curl commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an optional LEMONADE_API_KEY and a Lemonade server URL, defaulting to http://localhost:8000 when the user does not specify one.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
