## Description:

Returns daily time-series data for a single Ozon Russia SKU, including sales, price, stock, rating, comments, and optional search visibility signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce analysts, operators, and agents use this skill to inspect one Ozon SKU over time and identify sales, price, stock, rating, or visibility changes. It supports trend validation, seasonality checks, and factual anomaly reporting without making purchasing recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a LinkFox API key and may guide users through phone/SMS login or payment flows when access or billing errors occur.

Mitigation: Prefer self-service key setup, avoid sharing API keys in chat or persistent shell profile files on shared machines, and review authentication or payment steps before proceeding.

Risk: Endpoint environment variables can redirect requests to non-default LINKFOX_* hosts.

Mitigation: Verify LINKFOX_* endpoint variables are unset or point only to trusted LinkFox hosts before running the scripts.

Risk: Full API responses, cache files, and possible QR-code images may be written to local linkfox directories.

Mitigation: Run the skill in an appropriate workspace and review or delete local response, cache, and payment QR artifacts when they are no longer needed.

Risk: The security verdict is suspicious and the security summary flags sensitive account, payment, credential, persistence, and automatic feedback behaviors.

Mitigation: Review the skill and scan results before installation, and install only when those behaviors are acceptable for the intended environment.

## Reference(s):

- [MPSTATS Ozon Product Trend API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses, tables, file paths, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses and cache files under a local linkfox workspace path; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
