## Description:

An intelligent event finder that searches for meetups and events based on your interests, tracks them, and reminds you before they happen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apresmoi](https://clawhub.ai/user/apresmoi)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to discover events that match their interests, maintain a local list of tracked events, and receive reminders for events they plan to attend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent scheduled searches.

Mitigation: Review the exact scheduled task before enabling automation and confirm how to pause, resume, or remove it.

Risk: The skill stores event preferences, location, schedule, tracked events, and reminders locally.

Mitigation: Use the declared meetup-planner workspace for stored data and remove stale preference or event files when they are no longer needed.

Risk: The security review notes that the skill may inspect installed skills outside its declared workspace.

Mitigation: Approve inspection only for the search or scraping tools needed for setup, and decline broad access to unrelated installed skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apresmoi/skills/meetup-planner)
- [GitHub repository](https://github.com/apresmoi/meetup-planner)
- [GitHub repository metadata](https://github.com/apresmoi/meetup-planner.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown event summaries, JSON workspace files, shell command snippets, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local preference, event, reminder, backup, and schedule configuration files under the declared meetup-planner workspace.]

## Skill Version(s):

0.1.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
