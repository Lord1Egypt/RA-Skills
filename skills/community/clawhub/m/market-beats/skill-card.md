## Description:

Market Beats retrieves and displays 24/7 finance news from sources such as Jinshi Data with near-real-time updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luokeer52](https://clawhub.ai/user/luokeer52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor time-sensitive finance news and market updates through a remote Prana service wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The thin client sends user messages, thread IDs, request IDs, and API credentials to the configured Prana endpoint.

Mitigation: Install only when the Prana service is trusted, use HTTPS endpoints, and avoid custom base URLs unless they are controlled by the deploying organization.

Risk: API credentials may be read from or written to config/api_key.txt.

Mitigation: Prefer environment-provided credentials, set PRANA_SKILL_SKIP_WRITE_API_KEY=1 when avoiding secret persistence, and keep config/api_key.txt out of source control.

Risk: Finance-news responses are remote service output, not locally verified market data.

Mitigation: Treat returned content as untrusted service output and verify important market information against authoritative sources before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luokeer52/skills/market-beats)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [skill.yaml](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON or text returned by the remote service and passed through by the thin client.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote responses may include thread, request, status, or recovery metadata; treat the content as service output rather than locally verified news data.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/skill.yaml lists 8.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
