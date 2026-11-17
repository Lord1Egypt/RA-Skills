## Description:

Deploys a pixel-art desktop pet with mini and garden modes, four explorable scenes, care mechanics, and walk animations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitezhiiii](https://clawhub.ai/user/whitezhiiii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent install or guide setup of a Python/Tkinter desktop pet with interactive scenes, care actions, and customizable pixel assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports undisclosed file, credential, and network behaviors.

Mitigation: Review the script before installation and document all files, credentials, endpoints, and transmitted data for users.

Risk: The script can download assets and poll third-party services at runtime.

Mitigation: Prefer a release that bundles assets, enables network features only after clear consent, and verifies TLS normally.

Risk: The script can read nearby identity/profile files, use NBW_API_KEY, and send chat context to a cloud endpoint.

Mitigation: Remove parent-directory identity reads, avoid ambient credentials by default, and require explicit user opt-in before sending chat context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whitezhiiii/skills/pixel-desktop-pet)
- [Cozy People Character Sprites](https://pixelfight.itch.io/)
- [CraftPix Background Tiles](https://craftpix.net/freebies/)
- [Runtime Asset Download Endpoint](https://raw.githubusercontent.com/whitezhiiii/desktop-pet/main/assets/)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or copy a Python/Tkinter script and required image assets in the user's target directory.]

## Skill Version(s):

11.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
