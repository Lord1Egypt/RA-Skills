## Description:

Price Import supports importing price data from images, text, or Excel, standardizes the source data, matches it to a product catalog, and imports confirmed prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[young0529](https://clawhub.ai/user/young0529)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to convert supplier price tables into product-catalog matches, review unmatched items, adjust matching rules, and confirm price imports before API submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process and upload pricing files and create import logs that may contain sensitive business data.

Mitigation: Confirm file-retention and deletion practices before deployment, and limit use to data sources approved for upload.

Risk: The workflow can affect product-catalog and price data through business API calls, including batch imports and product creation paths.

Mitigation: Require matched-only imports or explicit human approval before creating products or importing unmatched records.

Risk: Evidence.security flags an insecure hard-coded HTTP import-log link.

Mitigation: Replace the HTTP IP-based link with an authenticated HTTPS endpoint before operational use.

Risk: The /fix requirements workflow expands beyond price import into persistent requirements-management files.

Mitigation: Separate or disable the /fix workflow unless requirements tracking is intended for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/young0529/skills/price-import)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, files, guidance]

**Output Format:** [Markdown reports, JSON-like configuration, API request guidance, and requirement documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces matching reports, import confirmations, matching-rule updates, and requirement-tracking documents.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
