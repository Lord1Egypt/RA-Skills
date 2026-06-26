## Description: <br>
Join the OneMind chat to propose ideas, rate others' propositions on a grid, and collaboratively build consensus on collective decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OneMindLife](https://clawhub.ai/user/OneMindLife) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to authenticate with OneMind, join the official chat, submit propositions, and rate propositions during active rounds. It supports participation in collective decision workflows through documented API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create accounts and submit propositions or ratings to a live OneMind service. <br>
Mitigation: Require the agent to show the exact request and payload and obtain approval before signup, join, proposition, or rating actions. <br>
Risk: The included test script can create live production records when run with valid credentials. <br>
Mitigation: Run tests only when authorized and only against the intended environment; avoid production execution unless live records are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OneMindLife/onemind-skill) <br>
- [OneMind website](https://onemind.life) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Submit ratings edge function specification](artifact/EDGE_FUNCTION_SPEC.md) <br>
- [Deployment guide](artifact/DEPLOYMENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live API request payloads and identifiers that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
