## Description:

Invention disclosure template, checklist, and Markdown-to-Word export (no third-party API token).

This skill is ready for commercial/non-commercial use.

## Publisher:

[windinwing](https://clawhub.ai/user/windinwing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, inventors, and patent workflow teams use this skill to draft invention disclosure Markdown, check required disclosure details, compare against prior art with patent-search, and export completed disclosures as downloadable Word files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export path can install an unpinned python-docx package at runtime, changing the local Python environment.

Mitigation: Install python-docx through a controlled, pinned dependency process before use, or disable runtime package installation in shared and sensitive environments.

Risk: Generated invention disclosure files can contain confidential patent information and may be saved to the configured upload directory.

Mitigation: Use an approved upload location, limit access to generated files, and remove exported disclosure files when they are no longer needed.

Risk: Patentability comments are only drafting support and are not legal advice.

Mitigation: Have a qualified patent attorney or agent review the disclosure before filing or relying on patentability conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/windinwing/skills/patent-disclosure)
- [Publisher profile](https://clawhub.ai/user/windinwing)
- [OpenClaw](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance and downloadable .docx or .md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The export command accepts completed Markdown content and may return a local download asset.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
