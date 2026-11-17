## Description:

News Sum Lite generates a lightweight Chinese daily news briefing from current news searches, saves it as Markdown, and sends it by email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liliangjie91](https://clawhub.ai/user/liliangjie91)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce a same-day Chinese news briefing covering default or requested topics, including summaries, source links, key takeaways, and a short outlook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a local report file and sends it as an email attachment automatically.

Mitigation: Require explicit confirmation showing the destination email address and attachment path before sending.

Risk: The email and attachment command has weak scoping for recipient and file path values.

Mitigation: Validate the recipient and attachment path and constrain output to the intended local archive directory.

Risk: The Markdown renderer dependency is invoked at runtime.

Mitigation: Pin or avoid the renderer dependency before installation or deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown news briefing with source links, plus shell commands for HTML conversion and email delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves the briefing to archive/news/brief/brief-yyyymmdd.md and uses the Markdown file as an email attachment.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
