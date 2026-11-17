## Description:

Deploys an end-to-end machine learning training pipeline across data preparation, training, evaluation, and serving agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML platform engineers use this skill to configure a four-agent Pilot Protocol pipeline for dataset preparation, model training, evaluation approval, and serving handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing role-specific packages or skills without review can introduce unintended dependencies.

Mitigation: Confirm the selected role, deployment prefix, peer hostnames, and exact packages before installation; prefer pinned or internally approved dependency versions for production use.

Risk: Datasets, model checkpoints, and inference metrics shared across agents may be sensitive.

Mitigation: Only exchange artifacts with trusted agents in the intended deployment and treat shared training, model, and inference data as sensitive.

Risk: The persistent ~/.pilot manifest can retain deployment details after setup.

Mitigation: Keep a record of the generated manifest so it can be audited or removed later.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-ml-training-pipeline-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Role-specific setup guidance depends on the selected role and deployment prefix.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
