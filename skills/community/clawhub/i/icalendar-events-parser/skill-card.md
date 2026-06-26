## Description: <br>
Parse .ics / iCalendar files or URLs, expand recurring events (RRULE), filter by date range / keywords, and return clean list of events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baptiste00001](https://clawhub.ai/user/baptiste00001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to parse local or remote iCalendar feeds, expand recurring events, filter them by date range or text fields, and return structured event data for scheduling or calendar analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided calendar URLs may expose private, internal, or tokenized calendar data to the agent environment. <br>
Mitigation: Use trusted calendar sources and avoid internal, private, or tokenized URLs unless the agent environment is intended to request them. <br>
Risk: Calendar titles, descriptions, and locations are untrusted data returned to the agent. <br>
Mitigation: Review event text before using it for downstream actions, publication, or automated scheduling decisions. <br>
Risk: Broad date ranges or recurring event feeds can produce large result sets. <br>
Mitigation: Provide bounded date ranges and check the returned count before passing results into later workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baptiste00001/icalendar-events-parser) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/baptiste00001) <br>
- [Project Homepage](https://github.com/baptiste00001/icalendar-events-parser) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with parsed calendar event objects and error objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, installs npm dependencies, accepts JSON input on stdin, can fetch user-provided calendar URLs, and can read .ics files from the OpenClaw workspace or the skill folder.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
