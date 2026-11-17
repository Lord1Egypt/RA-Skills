## Description:

Use the oo CLI to read and manage Memberstack member records and plans through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to retrieve Memberstack member information, verify tokens, and manage member accounts and free plans through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified downloads, and the CLI may make broader changes to agents than this skill documents.

Mitigation: Review the CLI installation before allowing automatic setup. To prevent startup skill synchronization, set OO_SKILLS_SYNC_DISABLED=1 as described in the oo CLI environment variable reference.

Risk: Memberstack data passes through OOMOL, and account changes can include deletion and Stripe cleanup.

Mitigation: Confirm the exact member, payload, and requested changes before writes; review deletion and Stripe cleanup flags carefully.

## Reference(s):

- [Memberstack](https://www.memberstack.com/)
- [Memberstack Admin REST API quick start](https://developers.memberstack.com/admin-rest-api/quick-start)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON command payloads and Memberstack action results, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include reads, writes, and destructive operations; write and destructive actions require confirmation as described in the skill.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
