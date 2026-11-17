## Description:

Input news text and use an LLM to analyze its impact on stock market sectors and concepts (bullish/bearish/neutral) along with the underlying logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fonilye](https://clawhub.ai/user/fonilye)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and AI agents use this skill to submit market news text and receive a concise sector and concept impact analysis with bullish, bearish, or neutral direction and supporting logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted news text and the EasyAlpha API key are sent to a remote analysis service.

Mitigation: Use only news text that is acceptable to share with the configured service, and avoid confidential research, sensitive prompts, or regulated data.

Risk: The script can use an arbitrary analysis server URL.

Mitigation: Configure only trusted HTTPS endpoints and avoid plain HTTP or unknown remote servers.

Risk: HTTPS certificate validation is disabled by default in the client script.

Mitigation: Require corrected HTTPS certificate validation before using the skill with important credentials or investment workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fonilye/skills/news-impact-analyzer)
- [Publisher Profile](https://clawhub.ai/user/fonilye)
- [EasyAlpha Service](https://easyalpha.duckdns.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Formatted terminal text from JSON or Markdown/text returned by the analysis service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an EASYALPHA_API_KEY; submitted news text is sent to the configured analysis server.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
