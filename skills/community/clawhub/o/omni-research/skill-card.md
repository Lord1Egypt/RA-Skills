## Description:

Multi-source deep research using the user's browser sessions to query Perplexity, Grok, and Gemini in parallel and synthesize the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmanchu](https://clawhub.ai/user/lmanchu)

### License/Terms of Use:


## Use Case:

Developers, analysts, and researchers use this skill to gather and compare answers from multiple subscribed AI research services through an existing browser session, then receive a combined research summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Chromium browser through CDP, so it can interact with accounts available in that browser profile.

Mitigation: Use a dedicated browser profile for this skill and keep unrelated sensitive accounts or confidential pages out of that profile.

Risk: API mode or synthesis can send the query and extracted results to the configured proxy endpoint.

Mitigation: Review ~/.config/omni-research/config.json before use and avoid submitting sensitive or confidential research topics.

Risk: The security verdict is suspicious because browser-only and zero-key framing can obscure the data flow through configured proxy services.

Mitigation: Review the skill and configuration before deployment, and restrict use to accounts and data approved for this workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lmanchu/skills/omni-research)
- [Publisher profile](https://clawhub.ai/user/lmanchu)
- [Perplexity](https://www.perplexity.ai/)
- [Grok](https://grok.com/)
- [Gemini](https://gemini.google.com/app)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown research report by default, or JSON containing the query and result when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-source sections, errors or timeouts for unavailable sources, and a synthesized summary when multiple sources return results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
