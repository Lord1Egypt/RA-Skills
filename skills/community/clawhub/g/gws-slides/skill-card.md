## Description: <br>
Google Slides: Read and write presentations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect and run Google Workspace gws slides commands for reading, creating, and updating Google Slides presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An untrusted or misconfigured gws CLI could expose or modify Google Workspace data. <br>
Mitigation: Install gws from a trusted source and review the shared authentication instructions and OAuth scopes before use. <br>
Risk: Google Slides write operations, especially batchUpdate, can change presentation content. <br>
Mitigation: Confirm presentation IDs and batchUpdate JSON before allowing edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-slides) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external gws CLI and shared Google Workspace authentication setup.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
