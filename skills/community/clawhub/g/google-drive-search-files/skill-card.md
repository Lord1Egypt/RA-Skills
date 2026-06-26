## Description: <br>
Atomic node skill to search for files in Google Drive using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an agent to locate files or folders in Google Drive through an already installed and authenticated gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local gog CLI that can access Google Drive. <br>
Mitigation: Use it only where the installed gog binary is trusted and authenticated to the intended Google account. <br>
Risk: Search results may expose private Google Drive file names or metadata inside the agent session. <br>
Mitigation: Review retrieved results before sharing them outside the session and avoid searching sensitive drives unless necessary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zvirb/google-drive-search-files) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [JSON returned by the gog CLI, with concise agent text when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gog binary to be installed and authenticated to the intended Google account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
