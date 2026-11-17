## Description:

Transforms a real product photo into a studio-quality ecommerce image, lifestyle scene, or marketplace-ready hero shot while preserving confirmed product details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce sellers and marketing teams use the skill to turn product photos into marketplace listings, lifestyle images, and promotional visuals. They can create a new composition or refine an accepted draft while keeping confirmed product details as the visual anchor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Beatra account permissions, and its authorization is shared with other Beatra skills.

Mitigation: Review the requested permissions before connecting. Understand that revoking this connection can interrupt other Beatra skills, and prefer a release with narrower permissions and safer disconnect behavior.

Risk: Installation analytics are reported automatically.

Mitigation: Review the analytics disclosure and controls before installing; choose a release with analytics controls if this reporting is not acceptable.

Risk: Chosen product photos are uploaded to Beatra, and approved image generation uses credits.

Mitigation: Review the selected photo and final image request before approval, and approve the paid generation only when its cost and upload are acceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/product-photo-studio)
- [Beatra skill page](https://beatra.ai/skills/product-photo-studio)
- [Image workflow](artifact/references/workflow.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Images, Files, Text]

**Output Format:** [Generated image files with artifact links and a brief text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One image per generation by default; image generation consumes credits after approval.]

## Skill Version(s):

0.3.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
