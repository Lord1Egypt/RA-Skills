## Description:

Operate Data247 through an OOMOL-connected account to check balances, screen and verify phone numbers, identify carrier types, and infer probable gender from first names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Data247 account can check account balance, screen or verify phone numbers, identify phone carrier types, and infer probable gender from a first name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic CLI setup runs remote code without checking its integrity or requesting separate approval.

Mitigation: Review and approve the CLI installation and any bundled skill changes separately; prefer a pinned, independently verified installation.

Risk: Submitted names and phone numbers are shared with OOMOL and Data247, and requests may incur charges.

Mitigation: Submit only details you intend to share with both services, and check applicable charges.

## Reference(s):

- [Data247](https://www.data247.com/)
- [Data247 API documentation](https://www.data247.com/api_user_manual)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON action requests and responses with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter, server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
