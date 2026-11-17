## Description:

Generates and edits images with Doubao Seedream through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request image generation or editing with a connected Doubao Seedream account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run remote installer code whose exact changes could not be inspected.

Mitigation: Review and install a fixed CLI release yourself before use, and require approval for setup changes.

Risk: CLI automatic skill synchronization can affect other installed agents.

Mitigation: Check the CLI's automatic skill synchronization settings before setup.

Risk: Image requests pass through OOMOL to the connected provider and may consume credits.

Mitigation: Consider connected-provider credit usage before submitting image requests.

## Reference(s):

- [Doubao Seedream product page](https://www.volcengine.com/product/ark)
- [Doubao Seedream API documentation](https://www.volcengine.com/docs/82379/1541523)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-doubao-seedream)

## Skill Output:

**Output Type(s):** [Images, API Calls]

**Output Format:** [Generated or edited images with JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image requests use the connected account and may consume credits.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
