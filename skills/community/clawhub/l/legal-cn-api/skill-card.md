## Description:

legal-cn-api provides a paid FastAPI service for AI agents and applications to search structured Chinese legal provisions backed by Meilisearch and x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengfelix](https://clawhub.ai/user/fengfelix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building legal AI agents and legal AI products can use this skill to deploy or call a search API for structured Chinese law articles without maintaining their own legal database. Operators can run the service with a local Meilisearch backend and paid search access.

### Deployment Geography for Use:

Global, for Chinese law search use cases

## Known Risks and Mitigations:

Risk: The release includes committed service credentials.

Mitigation: Remove the credential file from the release, rotate the exposed credentials, and load secrets from a deployment secret manager or environment variables.

Risk: Paid deployments may continue in open-access mode if payment configuration is missing or initialization fails.

Mitigation: Fail closed for paid search routes when x402 configuration or initialization is invalid, and alert operators before serving traffic.

Risk: Default Meilisearch keys, floating dependency ranges, and a floating container image can weaken deployment security and reproducibility.

Mitigation: Require a unique Meilisearch master key, pin reviewed package versions, and pin the Meilisearch image to a vetted version or digest.

Risk: Database update and import flows can replace the search index and ingest externally pulled legal data.

Mitigation: Run updates in staging first, keep index backups, review upstream data changes, and restrict who can run import or update jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengfelix/skills/legal-cn-api)
- [Initial legal corpus source](https://github.com/pengxiao1997/china_law)
- [Publisher profile](https://clawhub.ai/user/fengfelix)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON API responses and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses include law title, article number, article title, content, effective date, category, score, and total result count.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
