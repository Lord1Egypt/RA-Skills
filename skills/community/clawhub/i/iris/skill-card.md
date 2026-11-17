## Description:

Iris reads a Gmail inbox, scores recent email by urgency and sender importance, drafts replies for the top five actionable messages, and writes a daily action report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use Iris to triage recent Gmail messages, identify priority items, prepare draft replies, and keep a local markdown report for daily follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Gmail credentials and email-derived content.

Mitigation: Use a Gmail app password, keep credentials in environment variables, and revoke the app password from Google Account settings when it is no longer needed.

Risk: The skill writes sender, subject, urgency, and draft-reply data to a local markdown report.

Mitigation: Run it only in a trusted working directory and avoid regulated or highly sensitive mail unless report writing is changed or disabled.

Risk: The documented install command uses system Python package installation.

Mitigation: Install and run the skill in a dedicated virtual environment.

## Reference(s):

- [Iris ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/iris)
- [Iris ClawHub homepage](https://clawhub.ai/occupythemilkyway/iris)
- [OccupyTheMilkyWay publisher profile](https://clawhub.ai/user/occupythemilkyway)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console output and markdown report with draft-reply text and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local inbox_report_<date>.md file containing email-derived sender, subject, priority, and draft-reply content.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
