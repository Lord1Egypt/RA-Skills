## Description: <br>
Opens the system map application and starts navigation to an address or coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samkeke](https://clawhub.ai/user/samkeke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to open a destination in the local map application for navigation on macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destination addresses or coordinates may be shared with the local map application and its map provider. <br>
Mitigation: Avoid sending sensitive home, work, or private coordinates unless the user is comfortable sharing them with the configured map provider. <br>
Risk: Navigation handoff only works where the host system can run the map-opening command in a GUI desktop session. <br>
Mitigation: Use this skill on macOS or another environment with an equivalent map URL handler and visible desktop session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samkeke/open-map) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local GUI desktop session and a system map handler such as Apple Maps.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter states 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
