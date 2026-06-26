## Description: <br>
Google Workflow: Announce a Drive file in a Chat space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using Google Workspace automation use this skill to ask an agent for the gws command and required inputs to announce a selected Drive file in a Google Chat space. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The command posts a real announcement to the selected Google Chat space. <br>
Mitigation: Before running it, verify the Drive file ID, Chat space, optional message, and active Google Workspace account, and follow the shared gws authentication guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-workflow-file-announce) <br>
- [gws-shared](../gws-shared/SKILL.md) <br>
- [gws-workflow](../gws-workflow/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command flags for Drive file ID, Chat space, optional message, and output format.] <br>

## Skill Version(s): <br>
1.0.12 (source: release metadata; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
