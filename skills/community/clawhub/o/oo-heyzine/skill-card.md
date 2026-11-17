## Description:

Manage Heyzine flipbooks and bookshelves through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can list and inspect Heyzine flipbooks and bookshelves, organize flipbooks, update sharing metadata, and delete flipbooks through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs execution of downloaded installer code and an installed CLI that were not verified in this review.

Mitigation: Review and approve CLI installation separately; prefer a verified, fixed release instead of running a download directly.

Risk: OOMOL handles the connected account and receives connector requests.

Mitigation: Use an account authorized for these requests. The oo CLI command reference documents OO_SKILLS_SYNC_DISABLED=1 to disable automatic skill synchronization.

## Reference(s):

- [Heyzine](https://heyzine.com)
- [Heyzine API documentation](https://heyzine.com/developers#apikey)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance, shell command examples, JSON payloads, and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Heyzine account and its permissions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
