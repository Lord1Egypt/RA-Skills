## Description:

Generates a Chinese-language PDF attachment for Apple App Store China ICP exemption requests after collecting the user's Team ID, legal account holder name, App ID, and application date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extrastu](https://clawhub.ai/user/extrastu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and App Store account holders use this skill to prepare the PDF attachment needed when requesting an ICP exemption for an app distributed through Apple's China storefront.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PDF generator can silently attempt to install a system font package.

Mitigation: Remove the package-install fallback or move font installation to an explicit setup step reviewed before deployment.

Risk: The workflow collects account-linked Team ID, legal name, App ID, and date values.

Mitigation: Confirm the user wants to generate the PDF before collecting these details and run the skill in an isolated, unprivileged environment.

Risk: Weak input controls may mishandle crafted markup-like characters in document fields.

Mitigation: Validate and escape user-provided fields before rendering them into the generated PDF.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/extrastu/skills/icp-exemption-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with a Python command and a generated PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects Team ID, legal account holder name, App ID, and application date before generating the PDF.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
