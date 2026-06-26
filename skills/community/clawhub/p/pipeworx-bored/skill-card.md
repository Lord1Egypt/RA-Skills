## Description: <br>
Beat boredom with random activity suggestions — filter by type (education, social, cooking) or group size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent builders use this skill to request random activity ideas or filter suggestions by category and participant count for apps, team-building flows, onboarding, or everyday boredom prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to an external Pipeworx MCP endpoint and requires curl for the documented example. <br>
Mitigation: Use it only when external activity-suggestion requests are expected, and review the endpoint and local command before running or configuring the MCP server. <br>
Risk: Maintainer or registry workflows can involve sensitive credentials or impactful moderation actions. <br>
Mitigation: Treat service credentials as sensitive and confirm any target, reason, and intended effect before running moderation or deletion commands. <br>


## Reference(s): <br>
- [Pipeworx Bored homepage](https://pipeworx.io/packs/bored) <br>
- [Pipeworx Bored MCP endpoint](https://gateway.pipeworx.io/bored/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Activity suggestion responses may include fields such as activity, type, participants, accessibility, and price.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
