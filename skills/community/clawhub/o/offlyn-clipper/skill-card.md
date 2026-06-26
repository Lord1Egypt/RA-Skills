## Description: <br>
Connects OpenClaw to Offlyn Clipper on macOS through a local MCP bridge so an agent can search saved Clipper notes and summarize the live meeting being recorded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelnishanth](https://clawhub.ai/user/joelnishanth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers who use Offlyn Clipper with OpenClaw use this skill to install and pair a local MCP bridge, search saved notes, retrieve note context, list Clipper chat presets, and recap the live meeting currently being recorded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give OpenClaw access to private Offlyn Clipper notes and live meeting recaps. <br>
Mitigation: Install only when that sharing is intended, use explicit Clipper-specific requests, and review Clipper's per-tool sharing settings. <br>
Risk: The MCP bridge stores local pairing credentials for continued access. <br>
Mitigation: Protect the local credentials file and remove it if OpenClaw should no longer remain paired with Offlyn Clipper. <br>


## Reference(s): <br>
- [Offlyn Clipper OpenClaw guide](https://clipper.offlyn.ai/openclaw.html) <br>
- [Offlyn Clipper ClawHub listing](https://clawhub.ai/joelnishanth/offlyn-clipper) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Node.js, OpenClaw, Offlyn Clipper running locally, and a paired local credentials file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
