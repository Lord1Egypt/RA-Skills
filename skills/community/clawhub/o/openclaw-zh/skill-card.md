## Description: <br>
OpenClaw UI localization skill for translating the OpenClaw Web Control UI and Chrome extension interface into Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoranke](https://clawhub.ai/user/zoranke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to apply Chinese localization assets to a local OpenClaw Web Control UI installation and to guide Chrome extension interface translation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent edits to local OpenClaw UI files. <br>
Mitigation: Run the translation script only when intentionally localizing OpenClaw, preview changes with dry-run mode when available, and keep the generated backups for rollback. <br>
Risk: The script targets the OpenClaw installation under /usr/lib/node_modules/openclaw. <br>
Mitigation: Confirm that this path is the intended OpenClaw installation before applying translations. <br>
Risk: Chrome extension documentation and file naming may not match exactly. <br>
Mitigation: Confirm the target Chrome extension file before manually editing extension files. <br>


## Reference(s): <br>
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) <br>
- [OpenClaw Chinese documentation path](/usr/lib/node_modules/openclaw/docs/zh-CN/) <br>
- [ClawHub skill page](https://clawhub.ai/zoranke/openclaw-zh) <br>
- [Publisher profile](https://clawhub.ai/user/zoranke) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces localization guidance and invokes bundled translation files/scripts; applying the script modifies local OpenClaw UI files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
