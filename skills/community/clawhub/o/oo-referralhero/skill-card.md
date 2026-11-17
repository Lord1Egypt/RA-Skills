## Description:

Use this skill to read, create, update, and delete ReferralHero data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and developers use this skill to manage ReferralHero campaigns, subscribers, rewards, and referrals through their connected account. It supports reading data and performing confirmed changes such as adding, updating, tracking, or deleting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded installation code without a separate approval step.

Mitigation: Review and approve installation separately; prefer a pinned, independently verified installer.

Risk: The connected OOMOL account mediates access to ReferralHero, including operations that can change or delete data.

Mitigation: Use appropriately limited permissions and retain the skill's required write and delete confirmations.

## Reference(s):

- [ReferralHero](https://referralhero.com)
- [ReferralHero API documentation](https://support.referralhero.com/integrate/rest-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON requests and connector results, summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results and action status; writes and deletions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
