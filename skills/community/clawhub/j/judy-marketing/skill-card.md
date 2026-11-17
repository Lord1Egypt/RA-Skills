## Description:

Judy Marketing helps a marketing agent discover and enrich leads, plan outbound campaigns, draft marketing content, and develop go-to-market strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and agent builders use Judy Marketing to coordinate lead discovery, contact enrichment, cold email, LinkedIn outreach, ABM campaigns, marketing copy, and go-to-market planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect and retain prospect contact data during lead generation and enrichment.

Mitigation: Require human review of recipient lists, minimize retained contact data, and apply an explicit retention policy before use.

Risk: The skill can support real outbound email, LinkedIn, and ABM outreach without clear approval safeguards.

Mitigation: Use dry runs by default and confirm anti-spam, privacy, and platform compliance before sending messages.

Risk: The artifact references an Apollo API key stored in a shell startup file.

Mitigation: Move the Apollo key to a proper secrets store and avoid exposing credentials in local startup files or generated outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szzg007/skills/judy-marketing)
- [szzg007 publisher profile](https://clawhub.ai/user/szzg007)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated marketing artifacts such as lead lists, campaign plans, copy drafts, and summary reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve contact enrichment and outbound marketing workflows that require human approval before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
