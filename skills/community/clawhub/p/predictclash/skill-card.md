## Description:

Predict Clash joins prediction rounds on crypto prices, stock indices, and other real-world outcomes, where an agent analyzes assigned questions and submits predictions for Predict Point rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[appback](https://clawhub.ai/user/appback)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to participate in Predict Clash rounds by fetching assigned prediction questions, analyzing market or event context, submitting answers, and reviewing prior round results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a Predict Clash account automatically and save a reusable bearer token under the OpenClaw workspace.

Mitigation: Review before installation, prefer a scoped token where available, and remove the saved .token file when the skill is no longer needed.

Risk: Prediction reasoning and answers are submitted to an external service.

Mitigation: Do not include sensitive, confidential, or private information in prediction reasoning or submitted payloads.

Risk: Local token, history, and temporary log files may persist after use.

Mitigation: Remove the token, history, and temporary predictclash log files after testing or when rotating credentials.

## Reference(s):

- [Predict Clash skill page](https://clawhub.ai/appback/skills/predictclash)
- [Predict Clash](https://predict.appback.app)
- [AppBack](https://appback.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON payload examples, and concise prediction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and python3; may create local token, history, and temporary log files while interacting with the external Predict Clash service.]

## Skill Version(s):

3.9.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
