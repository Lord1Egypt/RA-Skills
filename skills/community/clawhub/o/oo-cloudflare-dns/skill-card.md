## Description:

Cloudflare DNS (cloudflare.com). Use this skill for ANY Cloudflare DNS request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare DNS, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this agent skill to inspect Cloudflare accounts, zones, and DNS records, and to create, update, or delete DNS records through a connected Cloudflare account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unchecked software whose documented behavior can make broader, lasting changes to agents.

Mitigation: Review CLI installation separately before allowing automatic setup, prefer an inspected and verified release, and consider the publisher-documented OO_SKILLS_SYNC_DISABLED=1 setting to disable startup skill synchronization.

Risk: Cloudflare credentials may allow access beyond the zones needed for the requested DNS work.

Mitigation: Restrict Cloudflare access to the intended zones and continue approving the exact DNS changes.

## Reference(s):

- [Cloudflare DNS API documentation](https://developers.cloudflare.com/api/resources/dns/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Cloudflare DNS skill release page](https://clawhub.ai/oomol/skills/oo-cloudflare-dns)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text responses, JSON connector payloads and results, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas; DNS writes and deletions require approval of the exact change.]

## Skill Version(s):

1.0.7 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
