## Description:

Automates KYC identity verification by securely managing and submitting identity documents, while asking user permission before accessing or uploading any file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seamao](https://clawhub.ai/user/seamao)

### License/Terms of Use:


## Use Case:

External users can use this skill to set up a local identity document vault and complete website KYC flows with per-file permission prompts, domain confirmation, form filling, and final submit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles passports, selfies, address proofs, and other highly sensitive identity material.

Mitigation: Create the identity vault with owner-only permissions, avoid shared or synced folders, and approve access only for specific files needed by a trusted KYC site.

Risk: The setup documentation references a mutable remote manifest download.

Mitigation: Prefer the bundled manifest template and verify any downloaded manifest source before placing personal information in it.

Risk: A malicious or mistaken website could cause identity material to be sent to the wrong destination.

Mitigation: Verify the exact domain and filename shown in each prompt, and continue only for KYC sites the user already trusts.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [KYC Vault on ClawHub](https://clawhub.ai/seamao/skills/kyc-vault)
- [seamao ClawHub profile](https://clawhub.ai/user/seamao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands, permission prompts, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before reading identity data, uploading each file, filling personal information, or submitting a KYC form.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
