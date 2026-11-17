## Description:

Search and explore ProductBoard features, products, and feedback

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertoamoreno](https://clawhub.ai/user/robertoamoreno)

### License/Terms of Use:


## Use Case:

Product and engineering teams use this skill to search a ProductBoard workspace, inspect feature and product hierarchy, and find customer feedback notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may be able to read ProductBoard product plans, feature details, and customer feedback data.

Mitigation: Install this skill only in workspaces where the agent is allowed to read that ProductBoard data.

Risk: The underlying ProductBoard connector and credentials determine the actual data available to the agent.

Mitigation: Scope connector credentials and ProductBoard permissions to the minimum workspace data needed for the intended use.

## Reference(s):

- [Productboard Search on ClawHub](https://clawhub.ai/robertoamoreno/skills/productboard-search)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance with tool names and example queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented ProductBoard search and lookup guidance; accessible data depends on configured ProductBoard connector credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
