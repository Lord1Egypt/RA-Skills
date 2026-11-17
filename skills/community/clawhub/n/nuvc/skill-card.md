## Description:

Score business ideas, get startup roasts, analyze markets, and extract structured data — powered by the same AI engine behind 250+ VC investment memos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuvcai](https://clawhub.ai/user/nuvcai)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, operators, investors, and agent users use NUVC to score business ideas, pressure-test startup pitches, analyze markets and competitors, review financial or pitch content, extract startup metrics, and list available NUVC models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted business ideas, pitch decks, financial details, and extracted metrics are sent to NUVC's external API.

Mitigation: Use only with content appropriate for NUVC processing; avoid confidential or regulated material unless NUVC's data handling terms are acceptable.

Risk: The skill uses shell-style command templates for user-provided business text.

Mitigation: Prefer an argument-safe runner that passes user content as a single argument array, and review commands before execution.

Risk: Business scores, roasts, market analysis, financial review, and extracted metrics may be incomplete or misleading.

Mitigation: Treat outputs as decision support and verify important claims, market data, financial conclusions, and investment judgments independently.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nuvcai/skills/nuvc)
- [NUVC API key registration](https://nuvc.ai/api-platform/keys)
- [NUVC API documentation](https://nuvc.ai/api-platform/docs)
- [NUVC website](https://nuvc.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown responses by default, with optional raw JSON when requested; setup guidance may include shell snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and NUVC_API_KEY; sends submitted business, pitch, financial, and metric content to NUVC's external API.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
