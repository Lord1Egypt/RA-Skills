## Description:

Convert a lightweight product request plus related signed-in pages into a product-confirmed requirements baseline published as one Feishu document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lza357](https://clawhub.ai/user/lza357)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and delivery agents use this skill to turn a lightweight product request and authenticated product-page investigation into one confirmed Feishu requirements document for downstream development and testing. It supports intake auditing, route-aware screenshot evidence, requirements drafting, product confirmation, publication, and read-back audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect authenticated product pages and capture screenshots that include account, phone, ID, secret, or other sensitive data.

Mitigation: Review the target pages and destination document or folder before use, and mask sensitive screenshot content before publication.

Risk: Publishing a Feishu requirements document before business confirmation could turn recommended or unverified behavior into an apparent product commitment.

Mitigation: Stop for explicit product manager confirmation, freeze only confirmed rules, and keep inaccessible page facts marked as Unverified.

Risk: Incomplete page evidence can make downstream requirements ambiguous or hard to audit.

Mitigation: Capture route evidence with the browser address bar, complete page evidence with copyable full URLs, and run the provided validation and read-back audit scripts.

## Reference(s):

- [Skill page](https://clawhub.ai/lza357/skills/product-requirement-delivery)
- [Intake card](references/intake-card.md)
- [UI evidence rules](references/ui-evidence-rules.md)
- [Fact source schema](references/fact-source-schema.md)
- [Deliverable contract](references/deliverable-contract.md)
- [Audit manifest example](references/audit-manifest.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown requirements baseline, Feishu document content, screenshot annotations, audit manifests, and validation command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit product confirmation before final Feishu publication; preserves observed, user-stated, recommended, and unverified facts as separate evidence classes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
