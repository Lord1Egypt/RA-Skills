## Description:

Searches, downloads, uploads, and manages Internet Archive (archive.org) items and metadata through the ia CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grill-glitch](https://clawhub.ai/user/grill-glitch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and archive operators use this skill to search public archive.org content, download item files, and perform authenticated uploads or metadata updates from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unpinned software.

Mitigation: Prefer manually installing a reviewed, pinned internetarchive package before enabling the install intent.

Risk: The skill can make public or account-changing uploads and metadata edits.

Mitigation: Review every upload path, identifier, collection, and metadata change before execution.

Risk: Internet Archive credentials may be exposed or misused on shared machines.

Mitigation: Use protected ia credentials and avoid configuring account credentials on shared machines.

## Reference(s):

- [Internet Archive](https://archive.org)
- [Internet Archive Developer Documentation](https://archive.org/developers/)
- [ia CLI Tool](https://github.com/jjjake/internetarchive)
- [Quick Reference](references/QUICK_REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON command results, and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install or call the ia CLI; upload and metadata operations require Internet Archive credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
