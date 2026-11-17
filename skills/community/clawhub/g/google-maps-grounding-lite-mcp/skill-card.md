## Description:

Google Maps Grounding Lite MCP for location search, weather, and routes via mcporter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanbaumann](https://clawhub.ai/user/ryanbaumann)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to configure and call Google Maps Grounding Lite MCP tools for place search, weather lookup, and route computation from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GOOGLE_MAPS_API_KEY is a secret and may be exposed through shared terminals, logs, screenshots, or copied command output.

Mitigation: Store the key in a private environment or secret manager, avoid echoing it in shared contexts, and redact command output before sharing.

Risk: The setup depends on the mcporter npm package and may write system-level MCP configuration.

Mitigation: Install mcporter from a trusted npm registry, prefer pinned or isolated installs, and review where --system configuration is stored before applying it.

Risk: Google Maps Grounding Lite is described as experimental and preview-limited, with documented request limits.

Mitigation: Design agent workflows with rate limiting, retries, and fallback behavior for preview availability or quota limits.

Risk: The artifact notes attribution and data-use constraints for user-facing output.

Mitigation: Include Google Maps links in user-facing results and use only with models that do not train on input data.

## Reference(s):

- [Google Maps Grounding Lite documentation](https://developers.google.com/maps/ai/grounding-lite)
- [Google Cloud API credentials](https://console.cloud.google.com/apis/credentials)
- [Google Maps Grounding Lite MCP endpoint](https://mapstools.googleapis.com/mcp)
- [ClawHub skill page](https://clawhub.ai/ryanbaumann/skills/google-maps-grounding-lite-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_MAPS_API_KEY and mcporter; generated guidance should preserve Google Maps attribution requirements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
