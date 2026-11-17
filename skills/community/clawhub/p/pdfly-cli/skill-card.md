## Description:

pdfly-cli helps agents produce command-line guidance for manipulating PDF files with the pdfly CLI, including compression, merging, splitting, rotation, signing, extraction, metadata inspection, and conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[overdue-lin](https://clawhub.ai/user/overdue-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document automation users, and agent operators use this skill to select pdfly commands for common PDF workflows such as merging pages, rotating ranges, extracting content, signing documents, and inspecting metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install examples may pull an unpinned pdfly package version.

Mitigation: Install a pinned, trusted pdfly version and use package hashes or an approved package mirror where available.

Risk: PDF signing examples can expose certificate or PDF passwords through command history, process listings, or logs.

Mitigation: Avoid literal passwords in commands; use safer local secret handling supported by the environment and clear sensitive shell history when needed.

Risk: OpenSSL verification workflows can export private key material without encryption.

Mitigation: Do not use unencrypted private-key export options for routine verification; restrict certificate file permissions and keep private keys encrypted.

Risk: In-place or destructive PDF operations can overwrite original documents.

Mitigation: Prefer explicit output files, retain backups, and verify output before replacing source PDFs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/overdue-lin/skills/pdfly-cli)
- [Page Range Syntax Reference](references/page-ranges.md)
- [Cat Command Reference](references/cat.md)
- [Rotate Command Reference](references/rotate.md)
- [PDF Signing Reference](references/sign.md)
- [pypdf documentation](https://pypdf.readthedocs.io/)
- [fpdf2 documentation](https://pyfpdf.github.io/fpdf2/)
- [endesive documentation](https://endesive.readthedocs.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-path-sensitive commands for local PDF inputs, outputs, certificates, and page ranges.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
