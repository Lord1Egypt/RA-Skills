## Description:

Osori helps agents manage a local project registry, find and switch projects, inspect Git and GitHub status, run registry health checks, and expose project-management workflows through Telegram slash commands and shell scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oozoofrog](https://clawhub.ai/user/oozoofrog)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Osori to keep local projects searchable, switch an agent into the right project context, inspect repository status, and manage project roots, aliases, favorites, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A registry-repair bug can rewrite the active project registry even when high-risk repair is supposed to be blocked.

Mitigation: Back up ~/.openclaw/osori.json before installation or repair, prefer /doctor without --fix or with --dry-run, and avoid relying on the high-risk gate until corrupt-registry recovery is fixed.

Risk: Project scans and fingerprint commands can inspect local paths and call external command-line tools such as gh and optional entire.

Mitigation: Use narrow scan paths, review configured roots before scanning, and ensure external CLIs are authenticated only for the intended accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oozoofrog/skills/osori)
- [README](README.md)
- [Doctor Safe Fix Guide](docs/examples/doctor-safe-fix.md)
- [Multi-root design](docs/multi-root-design.md)
- [Entire CLI](https://entire.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and command output, with optional JSON for doctor checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or update a local registry file and may invoke git, gh, mdfind or find, and optional entire commands depending on the requested workflow.]

## Skill Version(s):

1.6.1 (source: server release metadata and target metadata, released 2026-02-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
