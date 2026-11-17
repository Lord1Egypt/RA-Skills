## Description:

Helps agents manage Namecheap DNS records by fetching existing records, merging changes, backing up state, and warning about hidden records before updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to prepare and review Namecheap DNS record changes, including record fetches, merges, backups, dry-run diffs, and ghost-record checks before applying updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Namecheap DNS updates can replace all records for a domain, including records that may be invisible to API reads.

Mitigation: Require dry-run or diff review, verify ghost records, keep backups, and avoid --force unless the DNS deletion impact is understood.

Risk: The release mixes unrelated project-management and assessment claims with DNS-management workflows.

Mitigation: Use the skill only for explicit Namecheap DNS work and do not rely on unrelated project-management or assessment claims.

Risk: DNS credentials and record data are sensitive operational assets.

Mitigation: Use environment-based credential handling, avoid hardcoding secrets, and review outputs before sharing logs or change summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/namecheap-dns-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with shell command examples and JSON result structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DNS change summaries, dry-run diffs, verification status, backup guidance, and warnings for destructive updates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
