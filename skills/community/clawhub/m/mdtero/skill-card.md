## Description:

Use when a user wants Mdtero to parse a paper from a DOI or URL into a structured Markdown package, translate a parsed paper while keeping structure, or download Mdtero task artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonbinc](https://clawhub.ai/user/jonbinc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse academic papers into structured Markdown packages, translate parsed papers while preserving structure, and retrieve Mdtero task artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parse and translate workflows send selected paper content or paper-source content to Mdtero's API.

Mitigation: Use the workflow only when sharing that content with Mdtero is acceptable; avoid confidential or proprietary manuscripts unless approved.

Risk: The optional local helper installer is separate from the ClawHub skill install.

Mitigation: Download and review the helper locally before running it, and verify publisher-provided checksums or signatures when available.

Risk: Mdtero API usage requires an API key.

Mitigation: Provide MDTERO_API_KEY through the local environment and avoid exposing it in shared logs, transcripts, or committed files.

## Reference(s):

- [ClawHub Mdtero Skill](https://clawhub.ai/jonbinc/skills/mdtero)
- [Mdtero Homepage](https://mdtero.com)
- [Mdtero Guide](https://mdtero.com/guide)
- [Mdtero Install Handoff](https://api.mdtero.com/skills/install.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and curl code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference API task IDs and downloaded paper artifacts such as paper_md, paper_bundle, paper_pdf, and translated_md.]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
