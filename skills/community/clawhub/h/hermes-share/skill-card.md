## Description: <br>
Share Hermes skills with other users by packaging skills as ZIP files, sending them through messaging platforms, or creating temporary expiring download links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almohalhel1408](https://clawhub.ai/user/almohalhel1408) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Hermes users use this skill to package one or more local Hermes skills, generate bilingual recipient instructions, share the package directly or through a temporary download link, and install received skill packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill archives may expose local skill contents when uploaded to temporary public file-sharing services. <br>
Mitigation: Inspect the generated ZIP before sharing, avoid sharing all skills unless each one is safe to disclose, and confirm sensitive files are excluded. <br>
Risk: Received packages may install executable skill code into the active Hermes skills environment. <br>
Mitigation: Verify the sender, inspect install.sh and included SKILL.md files before installation, and consider staging received files outside the active skills directory first. <br>


## Reference(s): <br>
- [Hermes Share on ClawHub](https://clawhub.ai/almohalhel1408/hermes-share) <br>
- [Bilingual Skill Frontmatter Convention](references/bilingual-frontmatter.md) <br>
- [Delivery Platform Quirks](references/delivery-platform-quirks.md) <br>
- [Share Message Template](templates/share_message.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [ZIP archives, Markdown recipient messages, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate bilingual README content and temporary download links for shared skill packages.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
