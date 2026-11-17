## Description:

Read glucose data from a Nightscout site. Use when the user asks for the current CGM reading, trend, recent readings, or Nightscout status. This skill is read-only and should not be used for portal login automation or write actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xeusoc](https://clawhub.ai/user/xeusoc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read current glucose, recent readings, and basic status from a configured Nightscout site. It supports read-only reporting of CGM values, trends, timestamps, and site status without modifying Nightscout settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads health-related CGM data from a Nightscout site, which can expose sensitive personal health information in URLs, command output, or logs.

Mitigation: Set NIGHTSCOUT_BASE_URL only to the user's own HTTPS Nightscout site and avoid sharing URLs or output in logs or untrusted environments.

Risk: The source documentation mentions an external current_bg.py shortcut that is not included in the validated artifact.

Mitigation: Use only the bundled scripts/nightscout_read.py helper unless the external shortcut is separately trusted and inspected.

Risk: Glucose readings may be misunderstood as treatment guidance.

Mitigation: Report readings plainly, keep medical wording careful, and avoid treatment recommendations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports glucose in mg/dL with trend and timestamp when available; does not provide medical advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
