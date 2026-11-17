## Description:

Use this skill when OpenStoryline is already installed and the user wants to start local MCP and Web services, create or continue editing sessions, send editing instructions, perform multi-turn re-editing, and verify rendered video outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anlittledy](https://clawhub.ai/user/anlittledy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run an already installed OpenStoryline environment, configure required model endpoints, start local services, manage editing sessions, and verify generated MP4 outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu helper can upload any readable local file using local Feishu credentials.

Mitigation: Use the sender only for reviewed generated video files, confirm the recipient before sending, and avoid exposing arbitrary file paths or sensitive directories to the agent.

Risk: Changing service hosts or file-delivery settings can expose local workflows beyond the intended environment.

Mitigation: Keep OpenStoryline services bound to 127.0.0.1 unless the user explicitly requests LAN or mobile access, and use trusted networks only when broader access is required.

## Reference(s):

- [OpenStoryline Use troubleshooting reference](artifact/reference.md)
- [OpenStoryline Use ClawHub page](https://clawhub.ai/anlittledy/skills/openstoryline-use)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session IDs, service URLs, generated MP4 paths, and Feishu delivery status when requested.]

## Skill Version(s):

0.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
