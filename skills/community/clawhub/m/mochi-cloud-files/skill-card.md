## Description:

Connect a WebDAV drive, list and compare a directory, upload or download files, check versions and produce integrity hashes. Use for WebDAV Cloud File Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and agents use this skill to manage files in a user-specified WebDAV collection: inspect listings, compare one local directory, transfer selected files, review version conflicts, and generate SHA-256 hashes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Version checks do not confirm deletion intent or guarantee recovery.

Mitigation: Review the exact deletion target and use credentials limited to the intended WebDAV collection.

Risk: The connection profile, credential environment variable, and .mochilab state contain private data.

Mitigation: Protect the profile, credential environment variable, and .mochilab state.

Risk: Unpinned installation may reduce reproducibility.

Mitigation: Pin the installer version when reproducible installation matters.

## Reference(s):

- [WebDAV action and input contract](references/input.md)
- [MochiLab homepage](https://mochilab.bz)
- [MochiLab assistant setup](https://mochilab.bz/Skills/Connect.aspx?lang=en)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-cloud-files)

## Skill Output:

**Output Type(s):** [JSON, Files, Analysis]

**Output Format:** [JSON operation receipts and directory plans, SHA-256 hashes, and selected transferred files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selective file transfers up to 50 MiB each; directory listings are limited to one collection depth.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
