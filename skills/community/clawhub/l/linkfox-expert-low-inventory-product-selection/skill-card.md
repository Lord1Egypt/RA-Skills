## Description:

An Amazon product-selection agent for asset-light sellers that finds FBM, self-fulfilled, low-inventory-pressure opportunities using monthly-sales, recent-listing, and inventory-risk constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers use this skill to screen FBM product opportunities with monthly sales of at least 300 units and recent listings, then review Top 10 previews and Excel exports. The skill can also apply profile-driven ASIN scoring to rank candidates by competition, lifecycle, profit health, and entry difficulty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle includes behavior that can persistently modify agent instructions.

Mitigation: Review or remove the instruction-patching script before use, and inspect any generated instruction changes before deployment.

Risk: Credential-bearing API traffic may be redirected through custom LINKFOX_* endpoint overrides.

Mitigation: Use trusted LinkFox endpoints only, and avoid custom endpoint overrides outside controlled testing.

Risk: Uploaded files receive public URLs.

Mitigation: Confirm files are intended for public access before upload, and do not upload private or sensitive content.

Risk: Scheduled tasks can create recurring cost and send notifications to configured destinations.

Mitigation: Confirm task frequency, expected cost, and notification recipients before creating or enabling scheduled tasks.

## Reference(s):

- [Skill release page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-low-inventory-product-selection)
- [Primary skill definition](artifact/SKILL.md)
- [Amazon product scout API parameter catalog](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [ASIN dynamic scoring example expectations](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [SellerSprite product search API](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [LinkFox file upload API](artifact/skills/linkfox-file-upload/references/api.md)
- [LinkFox task scheduler API](artifact/skills/linkfox-task-scheduler/references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown previews with shell-command invocations, JSON summaries, and Excel .xlsx exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product-selection results are constrained to Top 10 conversation previews plus Excel files; scoring exports include dimension scores, weighted totals, recommendation grades, and rejection reasons.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
