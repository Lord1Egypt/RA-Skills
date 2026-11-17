## Description:

Queries 12306 high-speed rail and train ticket availability with no API key, including train schedules, seat availability, station matching, and multi-date comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianbo1110-cjb](https://clawhub.ai/user/jianbo1110-cjb)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and agents use this skill to check train options between Chinese railway stations, compare availability across dates, and summarize train number, timing, duration, booking status, and seat availability before using official 12306 channels for purchase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries contact 12306 public railway endpoints with the requested route and date.

Mitigation: Use the skill only when sharing those route and date details with 12306 public services is acceptable.

Risk: Ticket availability can change rapidly and the skill does not purchase tickets.

Mitigation: Confirm final availability and complete any purchase through the official 12306 website or app.

## Reference(s):

- [12306 official rail query service](https://kyfw.12306.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with command examples and train availability summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs train number, departure and arrival stations, times, duration, booking status, and available seat classes; ticket availability changes in real time.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
