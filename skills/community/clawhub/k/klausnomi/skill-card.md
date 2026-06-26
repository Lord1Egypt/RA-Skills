## Description: <br>
Engage in conversations with Nomi AI companions via the bundled Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bezko](https://clawhub.ai/user/bezko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use KlausNomi to list Nomi companions, exchange direct or room-based messages, retrieve profiles, and save avatars while keeping reusable non-secret context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected conversation text, room notes, and prompts to Nomi using a Nomi API key. <br>
Mitigation: Do not include secrets or regulated/confidential data unless the user intends to share it with Nomi. <br>
Risk: Room updates or deletions can change Nomi room state. <br>
Mitigation: Confirm room updates or deletions before running the corresponding CLI commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bezko/klausnomi) <br>
- [Project Homepage](https://github.com/openclaw/klausnomi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; the bundled CLI returns plain text, JSON, and avatar image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and NOMI_API_KEY; room and avatar operations may create or update local state under ./nomi/.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
