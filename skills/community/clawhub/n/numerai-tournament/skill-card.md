## Description:

Autonomous Numerai tournament participation — train models, submit predictions, and earn NMR cryptocurrency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obekt](https://clawhub.ai/user/obekt)

### License/Terms of Use:


## Use Case:

Developers, data scientists, and trading researchers use this skill to participate in the Numerai tournament by setting up credentials, downloading data, training LightGBM models, validating predictions, and submitting predictions or model uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Numerai credentials can authorize prediction or model submissions in a cryptocurrency tournament where staked NMR can be lost.

Mitigation: Prefer environment variables or a secret manager, use zero stake until performance is intentionally accepted, and review each upload before submission.

Risk: Pickle or cloudpickle model files can execute unsafe code if they come from an untrusted workspace.

Mitigation: Only load model pickle files that were created in a trusted workspace and keep dependency versions pinned for the Numerai runtime.

## Reference(s):

- [Numerai](https://numer.ai)
- [Numerai account and API keys](https://numer.ai/account)
- [Numerai Tournament skill page](https://clawhub.ai/obekt/skills/numerai-tournament)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate setup, training, validation, and submission instructions; authenticated submissions require Numerai credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
