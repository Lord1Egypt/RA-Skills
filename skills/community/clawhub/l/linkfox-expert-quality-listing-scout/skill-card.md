## Description:

精品铺货专家 helps Amazon sellers find high-quality listing opportunities by filtering SellerSprite product data for fast BSR growth, recent launch dates, and ratings of 4.0 or higher.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and e-commerce operators use this skill to scout quality product opportunities, compare sorting strategies, export Excel results, and optionally run a second-pass ASIN scoring workflow based on seller preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broader LinkFox automation may create persistent scheduled tasks or incur repeated execution costs.

Mitigation: Review the requested schedule and estimated cost before enabling recurring tasks, and keep task permissions narrowly scoped.

Risk: The bundled upload workflow can publish local files through public URLs.

Mitigation: Upload only files that are intended for public sharing and avoid sensitive local files.

Risk: API keys and endpoint override environment variables can expand access or route requests to untrusted hosts.

Mitigation: Use a dedicated low-privilege API key and set endpoint overrides only for trusted hosts.

Risk: The bundled patching script can make persistent changes to agent instruction files.

Mitigation: Run instruction-file patching only when persistent behavior changes are intended and backups or version control are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-quality-listing-scout)
- [SellerSprite product search API reference](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [Amazon product scout API parameter catalog](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [ASIN dynamic scoring example expectations](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [File upload API reference](artifact/skills/linkfox-file-upload/references/api.md)
- [LinkFox scheduled task API reference](artifact/skills/linkfox-task-scheduler/references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown summaries with shell commands and generated Excel, JSON, or CSV file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The main quality listing workflow is Excel-only and should not produce HTML reports.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
