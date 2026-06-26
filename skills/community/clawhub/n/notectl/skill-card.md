## Description: <br>
Manage Apple Notes via AppleScript CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainbat](https://clawhub.ai/user/rainbat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Notectl to list, inspect, search, create, and append Apple Notes from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Listing, showing, or searching notes can expose private note titles or contents. <br>
Mitigation: Use the skill only when Apple Notes access is intended, and review commands before exposing note output to an agent session. <br>
Risk: Add and append commands modify Apple Notes. <br>
Mitigation: Confirm the target note, folder, and text before asking an agent to run note-changing commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rainbat/notectl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for Apple Notes operations; command output may include note titles, folder names, note contents, or mutation status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
