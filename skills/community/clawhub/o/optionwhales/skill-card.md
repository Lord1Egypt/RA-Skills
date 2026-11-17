## Description:

Query real-time option flow intelligence and generate AI-powered trade analysis reports for unusual options activity, institutional positioning, derivatives sentiment, and AI trade report workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psdsam-niuniuking](https://clawhub.ai/user/psdsam-niuniuking)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure agents for OptionWhales option-flow analysis, unusual options activity review, momentum lookups, account usage checks, and AI-generated trade report retrieval. It is intended for US equity options workflows that require authenticated API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, report requests, user identifiers, and any orders JSON are sent to external services trusted by this skill.

Mitigation: Use revocable least-privilege tokens, prefer a pseudonymous user_id where possible, avoid unnecessary personal data in orders files, and rotate keys if redirects or logs may have exposed credentials.

Risk: AI-generated BUY, SELL, or HOLD trade reports may be incomplete, stale, or unsuitable for a user's financial situation.

Mitigation: Treat generated reports as decision support, require human review before trading, and compare recommendations with independent market, risk, and compliance checks.

Risk: Results can be limited by account tier, rate limits, service availability, or US-equity-options-only coverage.

Mitigation: Check quota, eligibility, usage, and service health before relying on outputs; disclose tier limits and avoid using the skill for crypto, forex, futures, Greeks calculation, or stock-price-only requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psdsam-niuniuking/skills/optionwhales)
- [Publisher profile](https://clawhub.ai/user/psdsam-niuniuking)
- [OptionWhales website](https://www.optionwhales.io)
- [OptionWhales API docs](https://www.optionwhales.io/developers)
- [Option Flow API base](https://api.optionwhales.io)
- [AI Report API base](https://ai-service-production-b44b.up.railway.app)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, shell commands, and JSON or Markdown responses from authenticated APIs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPTIONWHALES_API_KEY for option flow and AI_API_TOKEN for optional AI reports; available data and streaming features depend on service tier and external API availability.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
