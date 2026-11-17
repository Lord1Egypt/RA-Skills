## Description:

Provides random or daily useless facts with sources and links for trivia enthusiasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Agents serving trivia users use this skill to fetch random or daily useless facts and return the fact text with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may contact gateway.pipeworx.io when a user asks for facts.

Mitigation: Avoid sending private information as tool arguments and use the skill only for trivia requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-uselessfacts)
- [Pipeworx useless facts MCP endpoint](https://gateway.pipeworx.io/uselessfacts/mcp)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Text containing a fact, source, source URL, and permalink]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill exposes random_fact for changing results and today_fact for a daily shared result.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
