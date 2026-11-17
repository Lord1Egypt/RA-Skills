## Description:

Test all configured models for availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmanrui](https://clawhub.ai/user/xmanrui)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check whether configured model providers respond successfully and to identify failed models, timeouts, or provider errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the healthcheck can contact every configured model provider and may consume quota or create provider-side logs.

Mitigation: Use the single-model option when cost, scope, or logging exposure should be limited.

Risk: The healthcheck reports provider errors, authentication failures, and timeouts that may need operational follow-up.

Mitigation: Review failed model names and error messages before changing configuration or credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown list with pass/fail status, duration, error details, and a final tally]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact each configured model provider unless the user requests a single model.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
