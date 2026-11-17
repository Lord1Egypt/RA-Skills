## Description:

Finds listed model API prices and free credits through Grandet, and helps users connect a chosen offer to an app on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanzohanzhe](https://clawhub.ai/user/hanzohanzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other API users compare listed prices and free-credit offers for a chosen model; with their confirmation, they can configure an app to use a selected provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Price lookups and optional installation receipts contact grandet.ai.

Mitigation: Review the data-sharing behavior before use and disable installation receipts if unwanted.

Risk: Connecting an offer can route future model requests to a different provider and spend credit there.

Mitigation: Only connect on request, review the proposed configuration change, retain the backup, and restore it if needed.

## Reference(s):

- [Grandet](https://grandet.ai)
- [ClawHub skill listing](https://clawhub.ai/hanzohanzhe/skills/grandet-api-price-finder)
- [Free credits guide](artifact/references/free-credits.md)
- [App connection guide](artifact/references/host-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Concise text or Markdown with links and optional setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price and credit lookups use Grandet data; app configuration changes require user confirmation.]

## Skill Version(s):

0.3.0-build.20261018.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
