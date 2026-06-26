## Description: <br>
Change OpenClaw Dashboard accent color with one sentence. Dynamically finds CSS/JS files and updates all accent CSS variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenzhaoxuan0](https://clawhub.ai/user/chenzhaoxuan0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to change the Dashboard accent color by asking an agent for a named color or a #RRGGBB hex value. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script modifies files inside the user's OpenClaw installation. <br>
Mitigation: Install only when comfortable with local dashboard asset changes, review the script first on important installations, and keep the request explicit. <br>
Risk: Broad color-change trigger phrases could cause an unintended dashboard theme update. <br>
Mitigation: Use explicit requests with a named color or #RRGGBB value, and confirm the target color before execution when the request is ambiguous. <br>
Risk: OpenClaw upgrades or reinstalls can overwrite the customized dashboard assets. <br>
Mitigation: Re-run the theme command after upgrading or reinstalling OpenClaw. <br>


## Reference(s): <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/chenzhaoxuan0/openclaw-dashboard-theme) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with a local shell command and a short status response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single local theme-change operation for OpenClaw dashboard assets.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
