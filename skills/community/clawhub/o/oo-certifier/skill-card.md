## Description:

Operate Certifier to read, create, and update credential data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to inspect Certifier credentials, designs, groups, and interaction history, and to create and send credentials when approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote code and make broader changes to agents without adequately explaining them.

Mitigation: Review and approve CLI installation separately, and verify the documented OO_SKILLS_SYNC_DISABLED=1 control for the chosen release.

Risk: Credential issuance sends credentials and requires trust in OOMOL's Certifier access and recipient data handling.

Mitigation: Keep approval required for issuing and sending credentials, and confirm the intended account and recipient before approval.

## Reference(s):

- [Certifier](https://certifier.io)
- [Certifier API documentation](https://developers.certifier.io/reference/authentication)
- [OO CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Certifier ClawHub page](https://clawhub.ai/oomol/skills/oo-certifier)

## Skill Output:

**Output Type(s):** [API responses, JSON, Guidance]

**Output Format:** [JSON action results with concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Certifier account and requested action.]

## Skill Version(s):

1.0.5 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
