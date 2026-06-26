## Description: <br>
Access Listonic shopping lists: list lists/items, add/check/delete items, and manage lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JeremyMahieu](https://clawhub.ai/user/JeremyMahieu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect and manage Listonic shopping lists from a command-line workflow, including adding, checking, unchecking, deleting, creating, and renaming list content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Listonic credentials and refreshed tokens in a local config file. <br>
Mitigation: Keep ~/.openclaw/credentials/listonic/config.json private with restrictive permissions, prefer token mode over password mode, and rotate or revoke credentials if the file is exposed. <br>
Risk: The skill uses unofficial reverse-engineered Listonic API endpoints that may change without notice. <br>
Mitigation: Confirm API behavior before relying on the skill for important workflows and expect commands to fail if Listonic changes its web API. <br>
Risk: Delete and rename commands can permanently change shopping lists or list items. <br>
Mitigation: Confirm destructive operations with the user before running delete-item, delete-list, or rename-list commands. <br>


## Reference(s): <br>
- [ClawHub Listonic skill page](https://clawhub.ai/JeremyMahieu/listonic) <br>
- [Listonic API endpoint used by the skill](https://api.listonic.com) <br>
- [Listonic OIDC token endpoint used by the skill](https://api2022auth.ts.listonic.com/identity/connect/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON from CLI commands, plus Markdown setup and command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a local Listonic credential file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
