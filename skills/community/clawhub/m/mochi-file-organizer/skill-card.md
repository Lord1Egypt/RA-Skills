## Description:

Create a read-only classification plan and SHA256 duplicate report for an explicitly named local folder without moving or deleting files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People who want to review a local folder can use this skill to produce an extension-based organization plan and identify files with matching sizes and SHA256 hashes. They can review the proposed paths and duplicate groups before making any separate file changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports include filenames, paths, sizes, and hashes that may be private.

Mitigation: Keep reports private and use an approved local model when report details must stay on-device.

Risk: A matching size and SHA256 hash identifies a duplicate candidate but does not prove a file is safe to remove.

Mitigation: Review each match and check backups and application references before considering any separate deletion.

Risk: Installing an unpinned latest release can change the code used for a scan.

Mitigation: Prefer a reviewed, pinned installer version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-file-organizer)
- [MochiLab homepage](https://mochilab.bz)
- [GitHub project directory (linked from README)](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-file-organizer)

## Skill Output:

**Output Type(s):** [JSON, Markdown]

**Output Format:** [A JSON file organization plan and a Markdown duplicate report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only recommendations with source-relative paths, file sizes, SHA256 hashes, extension-based categories, proposed paths, duplicate groups, and skipped-path reasons.]

## Skill Version(s):

1.0.1 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
