## Description:

Use Mistral AI through an OOMOL-connected account for data access, model operations, and file processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to access Mistral AI through an OOMOL-connected account for conversations, agents, models, files, libraries, moderation, OCR, and related tasks. Confirm state-changing or destructive actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some state-changing actions are presented as safe reads, and downloaded installation code may run without a clear approval step.

Mitigation: Review before installing; use a verified, user-managed CLI installation, check automatic skill synchronization, and require confirmation for document reprocessing, conversation restarts, billable generation, writes, and deletions.

Risk: Using the connector involves entrusting credentials and content to OOMOL.

Mitigation: Consider which credentials and content you entrust to OOMOL.

## Reference(s):

- [Mistral AI API documentation](https://docs.mistral.ai/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Mistral AI](https://mistral.ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and structured API responses summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may create, update, upload, or delete Mistral AI data.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
