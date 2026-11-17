## Description:

Analyzes meeting transcripts to determine whether the discussion could have been handled as an email and returns filler-word counts and decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to evaluate meeting transcript text and decide whether a meeting could have been replaced by an email. It also reports filler-word counts to help summarize meeting quality signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts may contain confidential, regulated, customer, credential, or highly sensitive business content.

Mitigation: Review provider privacy and retention practices before use, and avoid submitting sensitive transcript text without organizational approval.

Risk: The skill sends user-provided meeting transcript text to an external MCP service.

Mitigation: Use only with transcripts that are appropriate to share with the disclosed external service.

## Reference(s):

- [Pipeworx could-have-been-email skill page](https://clawhub.ai/brucegutman/skills/pipeworx-could-have-been-email)
- [brucegutman publisher profile](https://clawhub.ai/user/brucegutman)
- [Pipeworx could-have-been-email MCP endpoint](https://gateway.pipeworx.io/could-have-been-email/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or text guidance with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns transcript analysis decisions and filler-word counts from an external MCP service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
