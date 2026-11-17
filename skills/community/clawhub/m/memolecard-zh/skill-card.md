## Description:

Automates the MocCard article-to-card workflow by opening the website, submitting a title and article content, selecting a card style, splitting the content into cards, and returning a ZIP download link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moccard](https://clawhub.ai/user/moccard)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to turn long articles into downloadable MocCard image-card packages through an automated browser workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article content may be submitted to moccard.com during the card-generation workflow.

Mitigation: Use only content that is appropriate to send to the MocCard service and allowed by the user's data-handling requirements.

Risk: Fallback download behavior can send readable browser cookies and card identifiers to the configured backup server.

Mitigation: Use the fallback path only with a trusted backup endpoint, or disable or review that configuration before running the skill.

Risk: The download workflow can remove matching ZIP files from the Downloads directory.

Mitigation: Run the skill with a dedicated download directory or preserve existing matching ZIP files before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moccard/skills/memolecard-zh)
- [MocCard website](https://www.moccard.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Shell execution output with a ZIP download URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download a ZIP archive to the configured browser download directory.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
