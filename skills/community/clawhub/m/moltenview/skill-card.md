## Description: <br>
Pushes persistent visual views such as charts, metrics, lists, and progress bars to the MoltenView Mac app when agent output benefits from a display outside chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldcote](https://clawhub.ai/user/goldcote) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use MoltenView to send structured dashboard-style views to a local Mac app for persistent visual summaries, live metrics, and reference displays outside the chat transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Views persist in the MoltenView app and may remain visible after the chat has moved on. <br>
Mitigation: Do not send secrets, credentials, personal data, or sensitive business content unless it is intended to remain visible; clear or replace views when they are no longer needed. <br>
Risk: The skill depends on a local MoltenView app and socket path being available. <br>
Mitigation: Confirm MoltenView is running and use the socket path from MoltenView Settings before sending or updating views. <br>


## Reference(s): <br>
- [MoltenView homepage](https://moltenrock.com) <br>
- [MoltenView on the Mac App Store](https://apps.apple.com/app/molten-view/id6742515562) <br>
- [ClawHub skill page](https://clawhub.ai/goldcote/moltenview) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MoltenView running locally on macOS and a Unix socket path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
