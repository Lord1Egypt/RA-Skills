## Description:

Track baby sleep, feeding, diapers, and growth via Huckleberry app API. Use for logging baby activities through natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronn](https://clawhub.ai/user/aaronn)

### License/Terms of Use:


## Use Case:

External users and caregivers use this skill with an agent to log and review baby sleep, feeding, diaper, and growth activity through Huckleberry-compatible CLI commands. The skill can ask for missing details before recording entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Huckleberry account credentials and child-health data.

Mitigation: Use reviewed dependency versions, avoid plaintext password storage where possible, and keep any credentials file private with restrictive permissions.

Risk: Write commands can change real Huckleberry records immediately.

Mitigation: Review generated CLI commands and required details before execution, especially for logging or updating activity records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaronn/skills/openclaw-huckleberry-skill)
- [Homepage listed in skill metadata](https://github.com/aaronn/openclaw-huckleberry-skill)
- [py-huckleberry-api dependency](https://github.com/Woyken/py-huckleberry-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or write live Huckleberry account records through a local Python CLI.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
