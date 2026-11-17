## Description:

Log meals, check nutrition progress, and manage calorie goals in the OpenCal app through an AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neikfu](https://clawhub.ai/user/neikfu)

### License/Terms of Use:


## Use Case:

External OpenCal users use this skill to let an AI agent search foods, log meals, summarize daily nutrition progress, and manage calorie and macro goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use authenticated access to read and change nutrition data.

Mitigation: Review before installing when OpenCal data is sensitive and use it only with a trusted OPENCAL_API_KEY environment.

Risk: The API destination can be weakly scoped when OPENCAL_BASE_URL is set.

Mitigation: Do not set OPENCAL_BASE_URL unless you control the endpoint.

Risk: Goal changes or deletions can affect user records if executed without clear confirmation.

Mitigation: Require the agent to confirm exact goal changes or deletions before running them.

## Reference(s):

- [OpenCal homepage](https://opencal.ai)
- [ClawHub skill page](https://clawhub.ai/neikfu/skills/opencal)
- [ClawHub publisher profile](https://clawhub.ai/user/neikfu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENCAL_API_KEY; uses curl and jq; OpenCal API rate limit is 100 requests/min.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
