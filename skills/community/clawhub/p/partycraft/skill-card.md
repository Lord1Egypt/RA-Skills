## Description:

Plan events with budgets, guest lists, and timelines. Use when organizing weddings, coordinating birthdays, managing vendors, drafting invitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and event organizers use Partycraft to create and track event plans, budgets, task lists, guest lists, timelines, and suggested checklists from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted event, task, guest, budget, or ID input can be interpreted as Python code by the bundled script.

Mitigation: Do not use the skill with untrusted or agent-supplied event text until the script passes values through arguments or JSON encoding instead of interpolating values into Python heredocs.

Risk: The skill writes local event data under ~/.partycraft/events.json.

Mitigation: Review the local storage behavior before installation and avoid storing sensitive event details unless that local persistence is acceptable.

## Reference(s):

- [Partycraft on ClawHub](https://clawhub.ai/bytesagain-lab/skills/partycraft)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text output and local JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists event data locally under ~/.partycraft/events.json.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
