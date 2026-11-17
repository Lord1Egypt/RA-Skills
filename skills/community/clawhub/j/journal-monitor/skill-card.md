## Description:

Monitors recent PubMed articles for specified journals using ISSN lookup and returns bilingual English/Chinese article metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenghan66](https://clawhub.ai/user/chenghan66)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and research assistants use this skill to check recent PubMed articles for selected journals, translate titles into Chinese, and prepare article metadata for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned Biopython dependency.

Mitigation: Pin and review the Biopython version before installation in controlled environments.

Risk: The skill contacts PubMed/NCBI for journal and article lookups.

Mitigation: Use it only where outbound access to PubMed/NCBI is permitted and expected.

Risk: The skill may create a Desktop report when many articles are found.

Mitigation: Ask for confirmation before file creation when tighter control over local writes is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenghan66/skills/journal-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown text with bilingual article metadata and optional report file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a Desktop report when more than 20 articles are found.]

## Skill Version(s):

1.0.11 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
