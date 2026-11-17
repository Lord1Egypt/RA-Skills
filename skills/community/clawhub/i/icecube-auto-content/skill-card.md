## Description:

IceCube Auto Content generates daily draft content templates for AI diary posts, technical shares, AI industry updates, Knowledge Planet posts, and related daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares521521-design](https://clawhub.ai/user/ares521521-design)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, community builders, and developers use this skill to draft recurring social and community content, including AI diary entries, technical tutorials, industry updates, and member-only posts. It also provides local shell scripts for generating dated Markdown drafts, a daily report, and workspace health summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafts may reuse real work, user interactions, or private context in public-facing content.

Mitigation: Require manual review and approval before publishing posts or replying to comments.

Risk: Generated reports may include workspace status metadata.

Mitigation: Review report contents before sharing and run the scripts only in workspaces where this metadata can be written locally.

Risk: Local diagnostic scripts are under-disclosed in the public skill description.

Mitigation: Inspect the bundled scripts before installation and execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ares521521-design/skills/icecube-auto-content)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown draft files and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates dated local Markdown drafts for content templates and reports when the bundled shell scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
