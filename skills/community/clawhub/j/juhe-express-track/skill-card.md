## Description:

Queries real-time package status and tracking history across supported domestic and international couriers through the Juhe Express API, using a local courier-code list for company lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up package delivery status from a tracking number and courier name or code, including a phone suffix when the courier requires it. The agent can summarize the current delivery state, signing status, and tracking events for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parcel identifiers, courier codes, the Juhe API key, and sometimes a 4-digit phone suffix are sent to Juhe for lookup.

Mitigation: Use the skill only when the user is comfortable sharing those values with Juhe, and provide phone suffixes only when the courier requires them.

Risk: API keys can be exposed if passed in command history or stored in tracked files.

Mitigation: Prefer the JUHE_EXPRESS_KEY environment variable and keep any scripts/.env file out of version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-express-track)
- [Juhe Global Express Tracking API documentation](https://www.juhe.cn/docs/api/id/43)
- [Juhe data service platform](https://www.juhe.cn)
- [Courier company code reference](references/express-company-list.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text tracking summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_EXPRESS_KEY environment variable or equivalent key configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
