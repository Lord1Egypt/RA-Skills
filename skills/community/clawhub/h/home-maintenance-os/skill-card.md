## Description: <br>
Tracks home appliances, service history, contractors, warranties, costs, and upcoming maintenance across one or more properties. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Homeowners and property managers use this skill to maintain a persistent local record of home systems, service visits, contractor details, maintenance schedules, warranties, and repair costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist household details, contractor contacts, service costs, warranties, and possibly addresses in home-data.json. <br>
Mitigation: Store only details needed for maintenance tracking, review confirmations after casual mentions, and periodically inspect or delete home-data.json if the record is no longer needed. <br>
Risk: Casual home-related statements may be interpreted as records to save, which can retain inaccurate or sensitive details. <br>
Mitigation: Review each logged confirmation and correct or remove records promptly when the captured details are wrong or too sensitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chris-openclaw/home-maintenance-os) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with structured updates to a local JSON data file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains home-data.json as the persistent local record when the host agent supports skill data storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and changelog, released 2026-05-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
