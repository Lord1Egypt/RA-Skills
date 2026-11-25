## Description:

Cloudflare (cloudflare.com). Use this skill for ANY Cloudflare request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage Cloudflare resources, including zones, DNS, R2, Workers, and Pages, through their connected OOMOL account. It guides the agent to check each action's schema and obtain confirmation before state-changing operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unverified remote installer and transfer of data to connector transit storage may create risks that read-only assurances do not make clear; the scan was partial because referenced local paths were missing.

Mitigation: Review the installer and its source before installation, confirm transit storage access and retention are acceptable for the data, and account for the incomplete scan evidence.

## Reference(s):

- [Cloudflare](https://www.cloudflare.com)
- [Cloudflare API documentation](https://developers.cloudflare.com/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON connector payloads and responses, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Cloudflare resource data; some actions change or remove account resources.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
