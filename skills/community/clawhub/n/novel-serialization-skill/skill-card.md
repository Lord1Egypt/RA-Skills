## Description:

Orchestrates AI-assisted novel writing and GitHub-based serialization, from world-building and character design through chapter drafting, continuity verification, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Authors and writers use this skill to plan novels, develop worlds and characters, draft chapters, track continuity, and prepare serialized releases on GitHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release automation is reported to have a command-execution flaw and may publish chapters without enforcing editorial approval.

Mitigation: Do not enable the release workflow until tag names are validated, tag text is passed through a quoted environment variable, and token permissions are reduced; review chapter attachments and actual editorial approvals before pushing a release tag.

Risk: Unpublished manuscripts may be exposed when pasted into AI services that are not trusted for that material.

Mitigation: Only submit unpublished manuscripts to AI services you have chosen to trust.

## Reference(s):

- [GitHub repository (server-resolved provenance)](https://github.com/JohnSmithfan/Novel-Serialization-Skill)
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/skills/novel-serialization-skill)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Novel planning documents, character and worldbuilding files, chapter drafts, continuity reports, and GitHub publishing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Novel content follows the user's requested language (English by default). The artifact documents GPL-3.0 infrastructure and CC-BY-NC-SA-4.0 generated content; verify the terms applicable to this release.]

## Skill Version(s):

0.1.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
