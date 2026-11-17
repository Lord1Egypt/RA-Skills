## Description:

Use TabAPI through an OOMOL-connected account to search the web and retrieve page, domain, DNS, and related data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to search the web and retrieve page, domain, DNS, and traffic data through their OOMOL-connected TabAPI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback executes remote installers and may change other agents' skill files without clearly limiting the effects or requiring approval.

Mitigation: Review the CLI installation and its effects separately, and approve setup before it runs, especially when it could change other agents' skills.

Risk: Requests use an OOMOL-connected account and may involve submitted data or usage charges.

Mitigation: Consider what you submit and any applicable usage charges before making requests.

## Reference(s):

- [TabAPI documentation](https://tabapi.com/docs)
- [TabAPI homepage](https://tabapi.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Markdown]

**Output Format:** [JSON or Markdown, depending on the TabAPI action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are returned by the selected TabAPI action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
