## Description:

Cloudflare Worker (workers.cloudflare.com). Use this skill for ANY Cloudflare Worker request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare Worker, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage Cloudflare Workers, scripts, builds, settings, and secrets through their connected Cloudflare account. It can also create, update, upload, or delete Worker resources when the user approves the specific change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback can run a remote CLI installer without prior approval.

Mitigation: Review and approve the installation before running it; prefer a pinned, verified release and check whether setup adds other agent skills.

Risk: Write and destructive actions can change, overwrite, or remove Cloudflare Worker resources.

Mitigation: Confirm the exact payload and effect before writes, and confirm the target and obtain explicit approval before destructive actions.

## Reference(s):

- [Cloudflare Workers documentation](https://developers.cloudflare.com/workers/)
- [Cloudflare Workers](https://workers.cloudflare.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured JSON responses summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Cloudflare account and the selected action.]

## Skill Version(s):

1.0.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
