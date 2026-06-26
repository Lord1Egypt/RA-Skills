## Description: <br>
MTA system train departures (NYC Subway, LIRR, Metro-North). Use when the user wants train times, schedules, or service alerts for MTA transit. Covers MTA Subway, LIRR, and Metro-North across the greater New York area. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up MTA Subway, LIRR, and Metro-North station departures, schedules, saved favorite stations, and active service alerts through the gotrain CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and depends on an external npm package that provides the gotrain command. <br>
Mitigation: Install only when the external npm package is trusted and appropriate for the deployment environment. <br>
Risk: Transit departures and alerts can be time-sensitive and may change after lookup. <br>
Mitigation: Treat results as current transit guidance and re-check live service information before making critical travel decisions. <br>


## Reference(s): <br>
- [gotrain ClawHub page](https://clawhub.ai/gumadeiras/gotrain) <br>
- [gumadeiras publisher profile](https://clawhub.ai/user/gumadeiras) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing guidance for installing and running the gotrain CLI; command output depends on the external npm package and live MTA transit data.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
