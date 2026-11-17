## Description:

Searches for and calls JisuAPI data interfaces from natural-language requests, including search, execute, and usage-statistics workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to discover the right JisuAPI interface from a natural-language request, execute the selected API with parameters, and review API usage, cost, and execution details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The one-step run mode can send user data and spend API quota on a remotely selected tool without enforcing confirmation or confidence checks.

Mitigation: Prefer the documented search then execute flow; confirm the selected tool, parameters, and match quality before execution.

Risk: A JISU_API_KEY with paid access or sensitive account permissions can expose account quota and billing to agent-driven calls.

Mitigation: Review account permissions before installation, avoid sending personal or confidential data unless necessary, and monitor JisuAPI usage charges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisuapi)
- [JisuAPI Agent documentation](https://www.jisuapi.com/agent/docs/)
- [JisuAPI Agent search API](https://www.jisuapi.com/agent/docs/search)
- [JisuAPI Agent execute API](https://www.jisuapi.com/agent/docs/execute)
- [JisuAPI Agent stats API](https://www.jisuapi.com/agent/docs/stats)
- [JisuAPI available tools](https://www.jisuapi.com/agent/docs/tools)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; command output is printed as formatted JSON.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
