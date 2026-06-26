## Description: <br>
Use kitchenowl-cli from terminal with pipx install, auth, and core read/write commands for KitchenOwl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apetersson](https://clawhub.ai/user/apetersson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to install, authenticate, and operate the KitchenOwl CLI for household, shopping list, recipe, and user-administration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and drives a third-party KitchenOwl CLI package and connects it to a configured KitchenOwl server. <br>
Mitigation: Install only when the kitchenowl-cli package and target KitchenOwl server are trusted. <br>
Risk: KitchenOwl authentication can store server URL, access token, refresh token, user, and saved defaults in the local KitchenOwl config file. <br>
Mitigation: Prefer interactive login, avoid putting passwords in shell history, protect the local config file, and use logout when finished. <br>
Risk: Create, edit, remove, delete, and bulk-change commands can modify account data. <br>
Mitigation: Review mutating commands before approval, start with read-only commands, and require confirmation before destructive operations. <br>


## Reference(s): <br>
- [KitchenOwl CLI Command Reference](references/commands.md) <br>
- [KitchenOwl CLI homepage](https://github.com/kitchenowl/kitchenowl-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request JSON CLI output when command results are consumed programmatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
