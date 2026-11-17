## Description:

A simple zero-dependency, environment-agnostic, and side-effect-free skill that helps users test if their OpenClaw instances can load skills correctly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adairli2504](https://clawhub.ai/user/adairli2504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to confirm that an OpenClaw instance loads and invokes skills by sending a message containing "marco" and checking that the response includes "polo".

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary messages containing "marco" may trigger the skill and add "polo" to the assistant response.

Mitigation: Install it where this trigger phrase is expected, or disable/remove the skill outside skill-loading tests.

## Reference(s):


## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text included in an assistant response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Triggered by user messages containing "marco"; security evidence discloses no local file, credential, network, dependency, or persistent-state access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
