## Description:

Generate HTML landing pages from templates with SEO optimization. Use when creating web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site builders use this skill to generate simple landing-page HTML, template suggestions, launch checklists, metadata extraction, SEO checks, and preview guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include unescaped title or description content when input is untrusted.

Mitigation: Use trusted title and description input, review generated HTML before publishing, and add HTML escaping before using third-party or user-submitted content.

Risk: The skill runs a local Bash helper that creates local state in the user's home directory.

Mitigation: Install and execute it only in environments where a small local shell helper and ~/.local/share/landing state are acceptable.

## Reference(s):

- [Landing skill page](https://clawhub.ai/bytesagain-lab/skills/landing)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text, checklist-style markdown, and HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local state under ~/.local/share/landing when the helper runs.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
