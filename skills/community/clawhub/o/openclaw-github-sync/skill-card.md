## Description:

Keeps an OpenClaw agent's non-sensitive context under version control in a separate Git repository for remote review, scheduled push syncs, and manual reviewed pullback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bradvin](https://clawhub.ai/user/bradvin)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to export selected workspace context to a private Git repository for review, grouped commits, and scheduled push synchronization. Manual pullback can restore reviewed Markdown and skill changes into the workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export manifest can copy private agent memory, skill code, and instruction files into a remote repository.

Mitigation: Use a private repository you control, apply least-privilege access, and narrow references/export-manifest.txt to sanitized paths such as memory/public/ and specific reviewed skills.

Risk: Manual pullback can overwrite active workspace Markdown and skill files, which may change future agent behavior.

Mitigation: Do not automate pull operations; use PULL_DRY_RUN and manual diffs before applying reviewed remote changes.

Risk: The heuristic secret scan may miss sensitive information or be bypassed by ignore rules.

Mitigation: Treat the scan as a final check, keep references/secret-scan-ignore.txt empty or tightly scoped, and sanitize exported content before syncing.

Risk: Environment loading reads references/.env for sync configuration.

Mitigation: Keep executable shell content out of references/.env and store only the minimum required sync configuration.

## Reference(s):

- [Project homepage from ClawHub metadata](https://github.com/bradvin/openclaw-github-sync)
- [README](README.md)
- [Export manifest](references/export-manifest.txt)
- [Commit grouping rules](references/groups.json)
- [Secret scan ignore rules](references/secret-scan-ignore.txt)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates or updates files in a private sync repository and can report sync, pull, status, or secret-scan results.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
