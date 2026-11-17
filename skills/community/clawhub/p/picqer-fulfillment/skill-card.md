## Description:

Provides JSON API commands to fetch Picqer dashboard KPIs, picklists, stock movements, and revenue data for order fulfillment monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnmcgucki](https://clawhub.ai/user/johnmcgucki)

### License/Terms of Use:


## Use Case:

Operations teams and agents use this skill to retrieve structured Picqer fulfillment dashboard data, including KPIs, picklists, stock movement categories, and revenue by client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Picqer tenant setting can redirect the API key to an unintended host.

Mitigation: Use a tightly scoped Picqer API key and validate or hardcode the exact Picqer tenant hostname before use.

Risk: The included auto-refresh file performs recurring authenticated syncs.

Mitigation: Do not run cron.ts unless recurring syncs are intended and monitored.

Risk: Dependency installation is less controlled without pinned dependencies and a lockfile.

Mitigation: Pin dependencies and add a lockfile before controlled deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnmcgucki/skills/picqer-fulfillment)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON-only success or error objects.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
