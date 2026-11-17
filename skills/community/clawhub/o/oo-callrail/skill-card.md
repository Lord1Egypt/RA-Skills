## Description:

Search and read CallRail accounts, calls, companies, and form submissions through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use the skill to retrieve CallRail account, call, company, and form-submission data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified code and may make broader changes to other agent skills.

Mitigation: Review the CLI setup, prefer a separately reviewed and pinned installation, and disable automatic skill synchronization if you do not want other skills changed.

Risk: Connecting CallRail authorizes OOMOL to handle the requested account data.

Mitigation: Connect only an account whose data access you intend to grant.

## Reference(s):

- [CallRail API documentation](https://support.callrail.com/hc/en-us/articles/5712444672909-CallRail-s-API-documentation)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [CallRail](https://www.callrail.com)
- [CallRail skill listing](https://clawhub.ai/oomol/skills/oo-callrail)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON connector responses and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
