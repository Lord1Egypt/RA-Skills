## Description: <br>
Operates Nylas through an OOMOL-connected account to read grants, calendars, and calendar events with the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with connected OOMOL and Nylas accounts use this skill to inspect Nylas grants, list calendars, and retrieve calendar events without handling raw tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nylas grant, calendar, and event data can contain sensitive account information. <br>
Mitigation: Confirm the specific account, calendar, and date range before retrieving data, and handle returned results as sensitive. <br>
Risk: The skill has a broad activation phrase for Nylas requests, which could lead to unintended connector use. <br>
Mitigation: Use it only for explicit Nylas tasks and verify the requested scope before running oo connector commands. <br>
Risk: Setup commands can install the oo CLI, start login, or open Nylas connection flows. <br>
Mitigation: Run setup only after a matching command failure or user request, and avoid proactive authentication or connection changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-nylas) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Nylas homepage](https://www.nylas.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live oo connector schemas before constructing action payloads; Nylas grants, calendars, and events may contain sensitive account data.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
