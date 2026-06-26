## Description: <br>
Google Calendar CLI helps agents manage Google Calendar events through the gog command-line tool, including listing, creating, updating, deleting, color support, OAuth setup, and scripting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and calendar users use this skill to generate gog CLI commands for checking availability, scheduling meetings, and maintaining Google Calendar events from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorized commands can read or change real Google Calendar data. <br>
Mitigation: Use a test or non-critical calendar while experimenting, review create/update/delete and looped commands before running them, and revoke Google Calendar access when it is no longer needed. <br>
Risk: OAuth client secrets and tokens grant calendar access if exposed. <br>
Mitigation: Protect OAuth client secrets and tokens, and install only if you trust the gog CLI and Homebrew tap. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-output command options for scripting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
