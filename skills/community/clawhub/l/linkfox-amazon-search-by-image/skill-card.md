## Description:

Finds visually similar Amazon products from a public image URL across eight Amazon marketplaces, with optional Keepa enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and product researchers use this skill to search for visually similar listings from a public image URL, compare products across supported Amazon marketplaces, and optionally enrich results with Keepa metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local image uploads produce publicly reachable image URLs.

Mitigation: Use non-sensitive images and require explicit confirmation before uploading a local file.

Risk: Account setup and recharge flows can involve phone codes and payment orders.

Mitigation: Run onboarding or payment commands only when the user explicitly requests LinkFox account setup or recharge.

Risk: API keys may be stored in shell profiles if users follow the setup examples directly.

Mitigation: Prefer a secret manager or session-scoped environment variable, and avoid committing or logging API keys.

Risk: Feedback reporting can send information to an external service without clear user consent.

Mitigation: Disable feedback reporting or require user confirmation before submitting feedback.

Risk: Repeated searches or Keepa enrichment can consume paid credits.

Mitigation: Confirm expected cost before retries, enrichment, or additional searches.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-search-by-image)
- [亚马逊-以图搜图 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, files]

**Output Format:** [Markdown tables and summaries, JSON API responses, and saved JSON data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large responses are summarized in stdout while full API responses are saved to a LinkFox session data directory.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
