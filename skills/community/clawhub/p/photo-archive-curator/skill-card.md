## Description:

Use when a phone or folder of thousands of photos needs culling, deduplication, and organization. Detects exact and near-duplicates (perceptual hashing), finds blurry shots, builds a burst-series keeper picker, and renames files into a dated folder tree using EXIF — no cloud, no uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Photo archive owners and curators use this skill to identify duplicate, blurry, and burst photos, review suggested keepers, and organize local collections into dated folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Even --scan overwrites a report, and applying organization can mishandle paired videos and RAW files.

Mitigation: Use only a backed-up copy, preserve reports separately, and avoid applying organization until paired files have been checked.

Risk: The advertised quarantine and deletion safeguards do not match the implementation.

Mitigation: Do not rely on the quarantine or deletion workflow; avoid deletion and verify changes on a disposable copy first.

## Reference(s):

- [Curation Guide](references/curation-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/voronindenis5/skills/photo-archive-curator)

## Skill Output:

**Output Type(s):** [Analysis, Text, Shell commands, Guidance]

**Output Format:** [CLI scan reports and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works with local archive paths; applying organization or deletion can mutate files.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
