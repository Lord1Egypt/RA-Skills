## Description:

Helps agents store local secrets and scripts, run stored workflows, and delegate sealed packages between trusted devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage local credentials and scripts, execute stored workflows, and transfer sealed scripts or packages between trusted devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local secret storage and script execution grant broad credential and execution authority; the stated plaintext protection boundaries may be overstated.

Mitigation: Review carefully before installation; use only trusted agents and scripts on a protected local account, and avoid highly sensitive production credentials until access scope and rotation are clear.

Risk: A local access token can provide access to the vault.

Mitigation: Protect the .mgc_token file as a vault credential and restrict local account access.

Risk: Reading secrets, running stored or sealed scripts, importing packages, or exporting plaintext archives can expose data or execute untrusted code.

Mitigation: Require explicit approval for each sensitive operation and inspect the source and destination before proceeding.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zkeviny/skills/mgc-meta-skill)
- [Project homepage (listed in manifest; import provenance unavailable)](https://github.com/zkeviny/MGC-Blackbox)
- [Project issue tracker (listed in manifest)](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Text and Markdown with inline commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to invoke local tools that store or read secrets, execute scripts, and package workflows.]

## Skill Version(s):

1.5.3 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
