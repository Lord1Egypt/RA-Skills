## Description:

Uses Xiaomi MiMo models' web search capability to answer real-time information queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enderxiao](https://clawhub.ai/user/enderxiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send current-information, news, documentation, and fact-checking queries to Xiaomi MiMo web search when a MIMO_API_KEY and supported model are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled search text is executed through a shell-based curl command, creating command-injection risk.

Mitigation: Use only in a constrained environment and avoid untrusted input until shell command construction is replaced with a native HTTP client or spawn/execFile argument array.

Risk: Search queries and returned content are sent to Xiaomi MiMo and could expose sensitive, personal, or proprietary data.

Mitigation: Avoid sensitive queries and avoid raw logging of secrets, personal data, or proprietary content.

Risk: The MiMo web-search API is paid, so uncontrolled calls can create unexpected costs.

Mitigation: Configure usage limits, cache repeated queries, and monitor API usage before enabling broad access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enderxiao/skills/mimo-web-search)
- [Xiaomi MiMo chat completions API endpoint](https://api.xiaomimimo.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON helper results or Markdown-formatted search responses with citation links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include success status, response content, usage metadata, errors, and citations; requires MIMO_API_KEY and paid MiMo API access.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
