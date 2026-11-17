## Description:

Runs Jogg lip sync using video and audio inputs, reuses tasks when available, and monitors status until completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joggai-tech](https://clawhub.ai/user/joggai-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit video and audio inputs to Jogg for lip-sync generation, reuse matching tasks when available, and check task status until a result URL is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected video and audio are uploaded to Jogg for processing using the configured API key.

Mitigation: Use the skill only with media approved for upload to Jogg, and use an API key with limited exposure where possible.

Risk: A skill-local .env file can provide default API settings if present.

Mitigation: Do not use a skill-local .env file from an untrusted source, and keep JOGG_BASE_URL unset or pointed at the legitimate Jogg API.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joggai-tech/skills/jogg-lip-sync)
- [Jogg API QuickStart](https://docs.jogg.ai/api-reference/v2/QuickStart/GettingStarted)

## Skill Output:

**Output Type(s):** [json, shell commands, guidance]

**Output Format:** [Machine-readable JSON result with progress logs on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task action, reuse status, task_id, status, result_url when successful, and error_message when failed.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
