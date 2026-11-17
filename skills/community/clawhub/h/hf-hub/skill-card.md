## Description:

Access Hugging Face Hub models, datasets, and spaces via the huggingface_hub Python library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noesis-boss](https://clawhub.ai/user/noesis-boss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to browse Hugging Face Hub models, datasets, and spaces, inspect model or dataset metadata, and transfer files to or from Hub repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HF_TOKEN can authorize access to private Hugging Face resources or upload operations.

Mitigation: Use a minimally scoped token, store it only in the approved secret setting, and rotate or revoke it if exposure is suspected.

Risk: The upload command can publish an unintended or sensitive local file to the selected Hugging Face repository.

Mitigation: Check the local path, repository ID, repository type, and destination path before running upload-file.

Risk: Live Hub content and library behavior can change across repositories, revisions, or huggingface_hub versions.

Mitigation: Pin huggingface_hub where reproducibility matters and specify trusted repository IDs and revisions for critical downloads.

## Reference(s):

- [Hugging Face access tokens](https://huggingface.co/settings/tokens)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with command-line examples and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads cache to ~/.cache/huggingface/; upload and download actions may transfer local or remote files using HF_TOKEN when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
