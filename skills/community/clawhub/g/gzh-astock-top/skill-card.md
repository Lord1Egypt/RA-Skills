## Description:

Retrieves dated rankings, account metrics, and latest article data for top A-share WeChat official accounts using RedFox data, then helps agents present results and manage account subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, investors, content operators, financial professionals, and data analysts use this skill to query A-share WeChat account rankings by date, review engagement metrics and latest article links, and track subscribed accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accepts a RedFox API key through multiple paths, including command-line arguments and a plaintext config file.

Mitigation: Prefer REDFOX_API_KEY from a secure environment or secret manager, avoid passing the key with --api-key, and avoid plaintext config files unless permissions are locked down.

Risk: Subscription management can persist local account choices and clear a category without an extra confirmation step.

Mitigation: Review requested subscription actions before execution and keep a backup or audit trail when local subscription state matters.

Risk: Account and article engagement metrics are sourced from RedFox ingestion and are not real-time.

Mitigation: Present the queried date, update-time note, and data-source caveat with returned rankings.

## Reference(s):

- [A股公众号大V API Guide](references/api_guide.md)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/gzh-astock-top)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and concise narrative backed by JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may update local subscription state when subscription actions are requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
