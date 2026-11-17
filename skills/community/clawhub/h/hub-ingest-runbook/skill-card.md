## Description:

A minimal, reproducible runbook for chaining a business-process tool (TaskFlow-style workspace orchestration) with the ClawHub CLI to turn processed digital content into a discoverable, installable resource-center entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this runbook to structure processed digital content, package it as a ClawHub skill, preview publication with a dry-run, publish it, and verify that it is discoverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing shares the package contents externally.

Mitigation: Confirm the folder contains only material intended for ClawHub and approved for external visibility before publishing.

Risk: A real publish can use the wrong account or slug if checks are skipped.

Mitigation: Run the documented dry-run, verify the slug and account identity, and only then perform the real publish.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/hub-ingest-runbook)
- [DESCRIPTION.md](artifact/references/DESCRIPTION.md)
- [workflow-handoff.md](artifact/workflow-handoff.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes identity checks, slug uniqueness checks, dry-run preview, publish, and search-verification steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
