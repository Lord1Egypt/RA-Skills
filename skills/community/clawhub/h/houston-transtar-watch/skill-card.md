## Description:

Poll Houston TranStar incidents RSS every 10 minutes and WhatsApp me when there are changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vijay-murugan](https://clawhub.ai/user/vijay-murugan)

### License/Terms of Use:


## Use Case:

External users such as Houston commuters and logistics teams use this skill to monitor Houston TranStar incident changes and receive concise traffic updates.

### Deployment Geography for Use:

United States (Greater Houston, Texas)

## Known Risks and Mitigations:

Risk: The server security review found that the registered runtime executes an external Python script outside the audited package.

Mitigation: Review and remediate the entry point before installation so it invokes only inspected package files.

Risk: The release advertises WhatsApp delivery, but the inspected code does not implement that delivery path.

Mitigation: Confirm notification delivery wiring before relying on alerts, or document the skill as producing local text summaries only.

Risk: The skill fetches traffic incidents from a live external RSS feed and writes a local incident snapshot.

Mitigation: Run it only where outbound access to Houston TranStar and local state writes under the skill state directory are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vijay-murugan/skills/houston-transtar-watch)
- [Houston TranStar incidents RSS feed](https://traffic.houstontranstar.org/data/rss/incidents_rss.xml)
- [Houston TranStar traffic site](http://traffic.houstontranstar.org)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text incident delta summary and JSON state snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns NO_CHANGES when no incident differences are detected; otherwise summarizes new, cleared, and updated incidents with each section capped at five listed items.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
