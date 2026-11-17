## Description:

Manage Gumroad and batch-publish digital products with the official CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, store operators, and commerce administrators use this skill to manage Gumroad products and run repeatable local digital-product publishing workflows through the Gumroad CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The batch publishing helper can upload local files named in an editable manifest.

Mitigation: Use only locally generated manifests, keep them in a trusted local state folder, and do not run publish against manifests from untrusted sources.

Risk: Products can be published before verification confirms the expected Gumroad state.

Mitigation: Use dry runs and one-product batches, verify each created product fully, and avoid --publish until upload path validation and verify-before-publish ordering are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stanestane/skills/gumroad-admin-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples and JSON manifest workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update local batch manifests when the helper script is used.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
