## Description:

Review an existing product main image for Amazon, Shopify, Etsy, or another marketplace and turn target listing requirements into a clear preflight card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers use this skill to check one existing product hero image against a named marketplace, region, and category, then review a concise preflight card and an optional single focused cleanup edit before listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags requested permissions and shared credential scope as broad for the stated image-preflight task.

Mitigation: Before installing, ask the provider to explain and narrow the permissions and shared credential scope.

Risk: Installation telemetry is reported without adequate user control.

Mitigation: Confirm what installation data is sent, where it goes, and whether telemetry can be disabled before installing.

Risk: Product image uploads are not clearly disclosed in the security assessment.

Mitigation: Confirm upload handling and disclose it to users; only submit images intended for processing by the service.

Risk: The security scan had partial coverage, so its evidence is incomplete.

Mitigation: Review the complete release package and obtain complete scan coverage before relying on the security assessment.

## Reference(s):

- [Marketplace main image preflight workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Installation registration](artifact/references/installation-registration.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [MCP connection](artifact/references/mcp-connection.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)
- [Beatra skill information](https://beatra.ai/skills/marketplace-main-image-preflight)
- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/marketplace-main-image-preflight)

## Skill Output:

**Output Type(s):** [Markdown, Images]

**Output Format:** [Markdown preflight card and one edited image artifact or result link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One existing image, one target listing scope, and at most one focused repair per approved request.]

## Skill Version(s):

0.2.5 (source: server-resolved release metadata, artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
