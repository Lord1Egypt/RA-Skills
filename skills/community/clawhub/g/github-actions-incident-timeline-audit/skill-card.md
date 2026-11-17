## Description:

Cluster failed GitHub Actions runs into incident windows by repo to expose outage duration, impact scope, and escalation severity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI reliability engineers use this skill to turn noisy GitHub Actions run exports into incident windows for review docs, dashboards, and CI fail gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Bash/Python script over files matched by RUN_GLOB.

Mitigation: Review RUN_GLOB before use so the script scans only intended GitHub Actions JSON exports.

Risk: FAIL_ON_CRITICAL can cause CI to fail when critical incidents are detected.

Mitigation: Enable FAIL_ON_CRITICAL only when failing the pipeline on critical incidents is desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-incident-timeline-audit)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text report or JSON incident summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and one or more critical incidents are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
