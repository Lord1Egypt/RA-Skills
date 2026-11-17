## Description:

Paper Checking guides agents through installing and using a Chinese-language plagiarism checking system for vertical and horizontal document similarity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, academic staff, and document-review teams use this skill to set up paper_checking.exe, configure comparison libraries, run vertical or batch cross-document checks, and interpret generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to download, build, or run external Windows code.

Mitigation: Use only a pinned and reviewed release or source checkout, avoid unverified precompiled binaries, and run it in a contained Windows environment.

Risk: The workflow processes papers, bids, internal documents, and generated reports that may contain sensitive information.

Mitigation: Restrict input and output folders, apply local data-handling controls, and treat RTF, CSV, and progress files as sensitive records.

Risk: Similarity results and threshold recommendations may be misleading if the comparison library, file conversion, or preprocessing is misconfigured.

Mitigation: Review configuration, supported file formats, comparison libraries, and generated reports before making academic, procurement, or compliance decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cn-big-cabbage/skills/paper-checking)
- [Project Homepage from ClawHub Metadata](https://github.com/tianlian0/paper_checking_system)
- [Java SDK Reference](https://github.com/tianlian0/duplicate-check-sample)
- [Commercial Version](https://xincheck.com)
- [Installation Guide](guides/01-installation.md)
- [Quickstart Guide](guides/02-quickstart.md)
- [Advanced Usage Guide](guides/03-advanced-usage.md)
- [Troubleshooting Guide](troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of a Windows executable and review of generated RTF or CSV reports.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
