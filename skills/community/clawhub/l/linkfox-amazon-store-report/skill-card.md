## Description:

Retrieves and downloads Amazon Seller Central store reports for inventory, orders, sales and traffic, FBA, settlements, returns, Brand Analytics, and related structured business data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and their agents use this skill to request, poll, download, decompress, and inspect Amazon Seller Central reports over selected marketplaces and date ranges. It is suited for bulk operational exports rather than small real-time order, product, or price lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle sensitive Amazon seller data, including API keys, seller identifiers, report requests, and downloaded business reports.

Mitigation: Install and run it only in environments where LinkFox is trusted for that data, and review access controls before using it with real seller accounts.

Risk: Downloaded reports may be served through a temporary unauthenticated local HTTP endpoint.

Mitigation: Keep report serving bound to 127.0.0.1, keep serve durations short, and disable the local HTTP download server when a file path is sufficient.

Risk: Feedback behavior can send task context to LinkFox.

Mitigation: Disable automatic feedback or require explicit user approval before sending feedback that may contain seller or report context.

Risk: The artifact includes account and payment onboarding flows beyond the narrow report retrieval task.

Mitigation: Use those flows only after clear user confirmation and review whether they are appropriate for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-report)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [Artifact README](artifact/README.md)
- [API reference](artifact/references/api.md)
- [Report types](artifact/references/report-types.md)
- [Common report types](artifact/references/report-types-basic.md)
- [Report request index](artifact/references/report-requests/README.md)
- [Report type request index](artifact/references/report-requests/types/README.md)
- [Amazon SP-API report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)
- [Amazon Selling Partner API report schemas](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON results; successful report runs save decompressed report files locally and may provide a temporary local download URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report output can include report IDs, document IDs, local file paths, file URIs, file names, file size, compression metadata, and short-lived local HTTP download details.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
