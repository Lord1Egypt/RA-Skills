## Description:

Sync local workspace directories and files to Notion pages using the notion-sync CLI or programmatic API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kitakitsune0x](https://clawhub.ai/user/kitakitsune0x)

### License/Terms of Use:

MIT

## Use Case:

Developers and workspace operators use this skill to initialize Notion sync configuration, preview changes, mirror selected local directories into Notion pages, manage ignore patterns, and check sync status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload the chosen directory's file contents and structure to Notion.

Mitigation: Run dry-run first, use a narrow sync directory, and confirm the target Notion page before syncing.

Risk: Local secrets or private configuration files may be included if the ignore list is incomplete.

Mitigation: Add explicit ignore patterns for .env files, credentials, keys, and private configs before syncing.

Risk: .notion-sync.json stores the Notion token plainly.

Mitigation: Treat the config file as sensitive, avoid committing it, and restrict file permissions where practical.

Risk: Untrusted repositories or symlinked content may cause unintended files to be synced.

Mitigation: Avoid syncing untrusted repositories with symlinks and review the dry-run output before upload.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kitakitsune0x/skills/openclaw-notion-sync)
- [Notion Integrations](https://notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline bash, TypeScript, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run guidance, ignore-pattern configuration, sync-status interpretation, and programmatic API examples.]

## Skill Version(s):

0.1.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
