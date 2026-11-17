## Description:

Konto helps agents query personal finance data from the Konto API, including accounts, transactions, investments, assets, loans, and financial summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angelstreet](https://clawhub.ai/user/angelstreet)

### License/Terms of Use:


## Use Case:

Developers and agents use Konto to answer personal finance questions by making authenticated, read-oriented API calls against a user's Konto service. It is intended for personal finance lookups such as net worth, balances, subscriptions, loans, investments, and recent transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive personal financial credentials with weak safeguards around the local secrets file.

Mitigation: Use a personal-scoped key, keep ~/.openclaw/secrets/konto.env private, and install only after trusting the Konto service and publisher.

Risk: KONTO_URL controls where authenticated financial requests are sent.

Mitigation: Set KONTO_URL only to the intended HTTPS Konto endpoint or to a deliberate local development server.

Risk: The helper script includes an analytics command outside the skill's declared personal scope.

Mitigation: Avoid placing an analytics-scoped key in this skill's secrets file unless analytics access is intentional.

## Reference(s):

- [Konto API Reference](artifact/api.md)
- [Konto ClawHub Skill Page](https://clawhub.ai/angelstreet/skills/konto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and jq examples plus shell helper commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Konto API key and KONTO_URL environment configuration for live API access.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
