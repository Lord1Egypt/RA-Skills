## Description:

Connects OpenClaw to local Offlyn Clipper so an agent can search saved notes, use chat presets, check bridge health, and summarize the live meeting currently being recorded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelnishanth](https://clawhub.ai/user/joelnishanth)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who run Offlyn Clipper on macOS use this skill to connect OpenClaw to local Clipper notes and live meeting context for recaps, note search, chat presets, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive local notes and live meeting context to OpenClaw.

Mitigation: Install only when the user trusts Offlyn Clipper and is comfortable sharing local notes and live meeting context with OpenClaw.

Risk: The integration stores reusable credentials and relies on a local socket path.

Mitigation: Review the credential file location, keep the socket path under the user's control, and avoid custom CLIPPER_SOCKET_PATH values unless they are intentional.

Risk: Broad prompts such as 'catch me up' may retrieve live meeting data.

Mitigation: Use live-meeting recap prompts deliberately and confirm Offlyn Clipper's per-tool sharing settings before using the integration.

## Reference(s):

- [Offlyn Clipper OpenClaw setup](https://clipper.offlyn.ai/openclaw.html)
- [ClawHub skill page](https://clawhub.ai/joelnishanth/skills/offlyn-clipper)
- [Publisher profile](https://clawhub.ai/user/joelnishanth)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local MCP setup, verification, troubleshooting steps, note-search guidance, and live-meeting recap guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
