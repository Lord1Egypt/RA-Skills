## Description:

Lurefish helps anglers plan lure-fishing trips, record catches, check weather and tides, choose lures, and review catch statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeansgit](https://clawhub.ai/user/jeansgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a lure-fishing assistant for trip planning, catch logging, location-aware spot research, lure selection, tide checks, and catch trend review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catch details such as dates, locations, lures, and notes may be stored locally under ~/lurefish/.

Mitigation: Install only when local storage of this fishing history is acceptable, and avoid recording sensitive location or personal details.

Risk: Weather, tide, map, or location-based searches may send query details to external services.

Mitigation: Provide weather or location details manually when privacy matters, and prefer HTTPS-backed lookup services.

## Reference(s):

- [Lurefish Skill Page](https://clawhub.ai/jeansgit/skills/lurefish)
- [Lure Knowledge](references/lures.md)
- [Target Species](references/species.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and locally stored JSON catch records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local catch data under ~/lurefish/ when the helper scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
