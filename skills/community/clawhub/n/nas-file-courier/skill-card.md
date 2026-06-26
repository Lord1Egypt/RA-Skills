## Description: <br>
Searches files on a NAS through rclone and Tailscale, then helps deliver selected files through supported messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TecFancy](https://clawhub.ai/user/TecFancy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to locate NAS files by keyword, type, path, or time range, confirm the intended file, and deliver it through Feishu, Telegram, QQ Bot, or a temporary Tailscale-only HTTP link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and transmit private files from the configured NAS remote. <br>
Mitigation: Install only for trusted agents with intended NAS read access, require explicit user confirmation before delivery, and send only permitted file types. <br>
Risk: Temporary HTTP sharing can expose sensitive files if it is used broadly or without isolation. <br>
Mitigation: Prefer native MEDIA delivery; use the HTTP fallback only on an isolated and authenticated Tailscale path and avoid it for sensitive files. <br>
Risk: A fixed temporary directory with wildcard cleanup can mix transfers or remove unintended files. <br>
Mitigation: Use a per-transfer temporary directory and clean it in a finally-style cleanup path after success or failure. <br>
Risk: Broad activation triggers could invoke the courier workflow for ambiguous file requests. <br>
Mitigation: Narrow activation to explicit NAS file-search or file-delivery requests and confirm the file name and size before sending. <br>


## Reference(s): <br>
- [Channel file sending reference](references/channel-file-send.md) <br>
- [HTTP temporary link reference](references/http-temp-link.md) <br>
- [rclone operations reference](references/rclone-ops.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and MEDIA file delivery lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local file paths, temporary download URLs, file metadata summaries, user confirmation prompts, and cleanup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
