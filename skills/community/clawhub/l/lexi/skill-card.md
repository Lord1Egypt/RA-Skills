## Description:

Lexi helps agents audit, catalog, and organize OpenClaw filesystem structures by identifying orphaned files, misplaced assets, stale artifacts, broken references, and structural inefficiencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcroebuck](https://clawhub.ai/user/mcroebuck)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Lexi to run structured filesystem audits, review file placement and reference integrity, and maintain a living catalog of important directories, projects, tools, and data stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad filesystem scans can surface sensitive paths or over-include areas that should not be reviewed.

Mitigation: Use a targeted scope in sensitive environments, confirm exclusions before scanning, and keep protected locations such as SSH, GPG, secrets, environment files, credentials, and system virtual filesystems out of scope.

Risk: File moves, archive operations, or reference updates can break workflows if proposed batches are accepted without review.

Mitigation: Require explicit user approval for each batch, archive files before deletion, check reference impact, verify old-path references after each batch, and stop on unexpected results.

Risk: Audit classifications may mislabel intentional, stale-looking, or rarely used files.

Mitigation: Present findings for collaborative review, accept user context when a file is intentional, and record those decisions in the catalog so future scans do not re-flag them.

## Reference(s):

- [Lexi ClawHub Skill Page](https://clawhub.ai/mcroebuck/skills/lexi)
- [Lexi Scanning Framework](artifact/scanning-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and catalogs with structured inventories, path lists, review prompts, action plans, and shell commands for approved filesystem operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only audit findings before any changes, then proposes approval-gated move, archive, reference-update, and catalog-update batches.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
