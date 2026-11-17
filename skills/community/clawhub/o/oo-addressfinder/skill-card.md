## Description:

Search, read, retrieve metadata for, and verify Australian and New Zealand addresses through Addressfinder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the agent to search Australian and New Zealand addresses, retrieve metadata for selected results, and verify or enrich addresses through Addressfinder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run changing remote installer code without a separate approval step.

Mitigation: Preinstall a reviewed CLI version, require approval before running installers, and check its automatic skill synchronization settings.

Risk: Address data is sent to OOMOL and Addressfinder when using the service.

Mitigation: Submit only addresses that you are permitted to share with both services.

## Reference(s):

- [Addressfinder API documentation](https://addressfinder.com/au/docs/api/overview)
- [Addressfinder Australia](https://addressfinder.com/au)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Address lookup and verification results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include address completions, selected-address metadata, and verification details.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
