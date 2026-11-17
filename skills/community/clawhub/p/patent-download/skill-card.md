## Description:

Downloads patent PDFs, retrieves patent information, and supports batch exports across multiple patent platforms with Google Patents as the preferred path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

Patent professionals, researchers, and agent developers use this skill to fetch patent PDFs or basic patent metadata from public and account-backed patent platforms. It is not positioned as a patent infringement, claims analysis, or validity assessment tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can auto-install unpinned Python packages and Chromium browser assets from the network.

Mitigation: Prefer manually installing reviewed, pinned dependencies in a virtual environment and running python cli.py directly instead of the auto-install wrapper.

Risk: Some platform paths use patent-platform credentials, make external network requests, and launch browser automation.

Mitigation: Use only trusted account credentials, confirm platform terms and access rights before automation, and prefer the public Google Patents path when it satisfies the task.

Risk: The security summary notes that one download path can write files outside the intended output folder from crafted input.

Mitigation: Pass normal patent identifiers only, choose trusted output directories, and review generated output paths before using downloaded files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/patent-download)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [Examples](references/examples.md)
- [Patent number formats](references/patent-number-formats.md)
- [Platform status](references/platform-status.md)
- [Accounts setup and ToS notes](references/accounts-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell command examples and downloaded patent files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write patent PDFs or metadata to a user-selected output directory.]

## Skill Version(s):

2.7.1 (source: frontmatter and changelog, released 2026-08-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
