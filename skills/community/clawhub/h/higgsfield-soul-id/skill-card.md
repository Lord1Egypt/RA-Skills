## Description:

Trains a reusable Higgsfield Soul Character from face photos for identity-faithful image and video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[higgsfield](https://clawhub.ai/user/higgsfield)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to prepare face-photo inputs, train a personalized Higgsfield Soul model, and use the returned Soul ID in later Higgsfield image or cinematic generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install the Higgsfield CLI through a remote installer command.

Mitigation: Review the installer source before execution and prefer a pinned, verified release or official package path.

Risk: The workflow uploads face photos to create a reusable identity model.

Mitigation: Use only photos the user has the right to upload and confirm explicit comfort with sending those photos to Higgsfield before training.

Risk: Training may proceed without enough privacy, consent, or account-plan clarity.

Mitigation: Confirm the authenticated account, paid-plan requirement, and intended downstream use before submitting a training job.

## Reference(s):

- [Photo Guide](references/photo-guide.md)
- [Soul Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/higgsfield/skills/higgsfield-soul-id)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Higgsfield CLI commands, account or plan checks, photo quality guidance, and a reusable Soul ID after training completes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
