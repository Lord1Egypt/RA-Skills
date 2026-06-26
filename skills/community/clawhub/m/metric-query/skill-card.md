## Description: <br>
Builds Aloudata semantic metrics query API requests by first looking up metric and dimension metadata from the Gateway API, then producing metrics query JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyujun](https://clawhub.ai/user/jackyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to convert natural-language metric questions into Aloudata CAN Gateway metric metadata lookups and metrics query request bodies. It is intended for workflows that need metric selection, dimension filtering, time constraints, temporary metric definitions, comparisons, proportions, rankings, or related semantic-layer query JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a CAN_API_KEY and outbound requests to the Aloudata CAN Gateway. <br>
Mitigation: Use a scoped key where available, keep the key in the configured environment variable, and review generated commands before execution. <br>
Risk: Metric filters, dimensions, or query bodies may contain sensitive business data sent to gateway.can.aloudata.com. <br>
Mitigation: Review generated request JSON before execution and avoid sending sensitive filters unless that data is appropriate for the Aloudata gateway. <br>
Risk: Incorrect metric or dimension names can produce misleading query results. <br>
Mitigation: Follow the skill behavior of querying Gateway metadata first and returning an empty JSON object when metric coverage or dimension compatibility is insufficient. <br>


## Reference(s): <br>
- [Aloudata homepage](https://aloudata.com/) <br>
- [ClawHub skill page](https://clawhub.ai/jackyujun/metric-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAN_API_KEY and outbound access to gateway.can.aloudata.com; Gateway metadata responses are described as plain text.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
