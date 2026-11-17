## Description:

TikHub (tikhub.io). Use this skill for ANY TikHub request — searching and reading data. Whenever a task involves TikHub, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to discover TikHub endpoints, inspect endpoint pricing and metadata, review account usage information, and invoke functional endpoints through an OOMOL-connected TikHub account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CLI installation commands execute remote installer code, whose exact behavior is unverified.

Mitigation: Review and use a vetted, pinned CLI installation; avoid running the installer until its source and behavior are trusted.

Risk: The required CLI can install additional agent skills through automatic synchronization, a behavior this skill does not explain.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to disable automatic skill synchronization when only this integration is wanted.

Risk: TikHub account access and endpoint use can expose account information or incur request charges.

Mitigation: Use minimum TikHub scopes, protect account and key information, and monitor request charges.

## Reference(s):

- [TikHub API documentation](https://docs.tikhub.io/)
- [TikHub](https://tikhub.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some actions require TikHub account path scopes; endpoint requests may incur charges.]

## Skill Version(s):

1.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
