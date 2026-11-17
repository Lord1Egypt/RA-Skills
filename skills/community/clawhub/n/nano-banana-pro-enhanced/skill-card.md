## Description:

Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro).

This skill is ready for commercial/non-commercial use.

## Publisher:

[steamb23](https://clawhub.ai/user/steamb23)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate new images, edit existing images, and manage non-blocking batch image jobs through Google's Gemini image API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch mode stores prompts, filenames, and job details locally until cleanup.

Mitigation: Avoid sensitive prompts in batch mode, review pending job records, and clear completed or stale HEARTBEAT and pending-job entries.

Risk: Batch retrieval can write image results to paths recorded or supplied for the job.

Mitigation: Use explicit safe output directories and run the skill in a restricted workspace.

## Reference(s):

- [Google AI for Developers](https://ai.google.dev/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files with terminal status text and saved file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports synchronous generation or editing, batch submission, and later batch-result retrieval.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
