## Description:

Search and read Tradebee product, group, language, and blog data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Tradebee languages, product groups, products, blog groups, and blogs through an OOMOL-connected account. It guides them to check each action's live schema before sending read requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute downloaded code whose contents and local changes have not been verified.

Mitigation: Review setup, install a verified CLI release yourself, inspect any bundled skill synchronization, and approve account connection separately.

Risk: Tradebee requests pass through OOMOL.

Mitigation: Review this disclosed data path before connecting the Tradebee account.

## Reference(s):

- [Tradebee homepage](https://www.tradebee.cn/)
- [Tradebee API documentation](https://open.tradew.com/documents/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)
- [Tradebee connection setup](https://console.oomol.com/connections/tradebee)
- [Tradebee on ClawHub](https://clawhub.ai/oomol/skills/oo-tradebee)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Tradebee data in JSON responses, with shell command examples and Markdown guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some list results are paginated; continue with pagination.next_page where provided.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
