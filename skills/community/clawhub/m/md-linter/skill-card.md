## Description:

Lint, check, and auto-fix Markdown files for tables of contents, broken links, YAML frontmatter validation, and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation owners, open-source maintainers, and agents use this skill to lint Markdown, generate or insert tables of contents, validate YAML frontmatter, check links, and format files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions fetch executable code from a mutable remote branch.

Mitigation: Install and run the bundled reviewed md_linter.py artifact or another pinned release artifact instead of downloading from the mutable main branch.

Risk: External link checking can make unrestricted network requests.

Mitigation: Use external link checking only on trusted Markdown or inside a network-restricted environment.

Risk: The CI verification harness can execute checks against package directories.

Mitigation: Avoid running ci/verify_product.py against untrusted package directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/itspremkumar/skills/md-linter)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can modify Markdown files in place when write or insert options are used; external link checking may perform network requests.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
