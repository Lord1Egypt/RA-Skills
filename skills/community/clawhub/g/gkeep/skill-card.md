## Description: <br>
Google Keep notes via gkeepapi. List, search, create, and manage notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VACInc](https://clawhub.ai/user/VACInc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to interact with Google Keep notes from a CLI, including listing, searching, reading, creating, archiving, trashing, pinning, and updating notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a reusable Google Keep authentication token at ~/.config/gkeep/token.json. <br>
Mitigation: Use a Google App Password, restrict local file access, and delete token.json or revoke the app password when access is no longer needed. <br>
Risk: The skill can create, archive, trash, pin, unpin, check, and append to Google Keep notes. <br>
Mitigation: Review note IDs and command arguments before running mutation commands; use list, search, or get first to confirm target notes. <br>
Risk: The skill depends on an unofficial Google Keep API that may break if Google changes the service. <br>
Mitigation: Confirm behavior after dependency or service changes, ideally with a non-critical account or small test note set before broader use. <br>


## Reference(s): <br>
- [ClawHub Google Keep skill page](https://clawhub.ai/VACInc/gkeep) <br>
- [gkeepapi project](https://github.com/kiwiz/gkeepapi) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Plain text CLI output and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gkeep CLI binary and a local Google Keep authentication token.] <br>

## Skill Version(s): <br>
1.0.3 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
