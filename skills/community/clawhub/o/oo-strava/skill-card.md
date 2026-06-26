## Description: <br>
Strava (strava.com). Use this skill for Strava requests, including reading, creating, and updating data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to work with Strava account data through the OOMOL connector, including activity, route, club, gear, segment, stream, upload, and athlete profile workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Strava account data through an OOMOL-connected account. <br>
Mitigation: Install only when comfortable connecting Strava through OOMOL and letting an agent read Strava data on request. <br>
Risk: Write actions can create or update activities, upload activity files, update athlete weight, or change segment starring state. <br>
Mitigation: Review and confirm exact write payloads before approving actions that change Strava data. <br>


## Reference(s): <br>
- [Strava homepage](https://www.strava.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-strava) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
