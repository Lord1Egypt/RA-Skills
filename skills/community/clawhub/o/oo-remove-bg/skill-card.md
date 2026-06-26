## Description: <br>
Operate remove.bg through an OOMOL-connected account to check account quota, remove image backgrounds, and submit improvement images via the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate remove.bg from an agent through an OOMOL-connected account. It supports checking account quota, removing backgrounds from URL or base64 images, and submitting improvement images after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected remove.bg account through OOMOL as an intermediary for sensitive credentials. <br>
Mitigation: Install only when the user is comfortable with OOMOL-mediated account access, and rely on server-side credential injection rather than handling raw tokens. <br>
Risk: Background removal may consume remove.bg credits and upload generated results to connector transit storage. <br>
Mitigation: Confirm the exact payload before credit-consuming actions and check account balance when cost or quota matters. <br>
Risk: Submitting improvement images sends source image data to the remove.bg improvement program. <br>
Mitigation: Request explicit user confirmation before running the write action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-remove-bg) <br>
- [remove.bg homepage](https://www.remove.bg) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL remove.bg connection](https://console.oomol.com/app-connections?provider=remove_bg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON, Files] <br>
**Output Format:** [Markdown with shell commands and JSON payloads; action responses may include JSON data and generated image or ZIP file outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before building action payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
