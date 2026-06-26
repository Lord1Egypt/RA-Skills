## Description: <br>
Automates batch uploads of game marketing assets to the mmgame operations platform through a logged-in browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xymhxy](https://clawhub.ai/user/xymhxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game operations staff and developers use this skill to guide an agent-driven browser session that uploads image and composite game assets to mmgame. It is intended for workflows where the user has already logged in, selected the target game, and prepared the asset files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may operate a logged-in mmgame account and upload or submit assets under that account. <br>
Mitigation: Confirm the account, target game, templates, files, and generated configuration before allowing browser automation to proceed. <br>
Risk: The artifact describes running a separate upload script, but no script is included in this package. <br>
Mitigation: Inspect any upload script separately before running it, and only execute scripts from a trusted workspace. <br>
Risk: Incorrect asset dimensions, file sizes, names, or submission timing can cause upload or review failures. <br>
Mitigation: Check each asset against the documented template requirements and review lead times before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xymhxy/mmgamexxyanguo) <br>
- [mmgame platform](https://mmgame.woa.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires workspace-accessible asset files and a logged-in mmgame.woa.com browser session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
