## Description:

Queries mobile or landline numbers across nine phone-marking platforms and summarizes platform hits, risk level, and call-handling advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengshukaihua](https://clawhub.ai/user/fengshukaihua)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check unfamiliar Chinese mobile or landline numbers for spam, fraud, marketing, delivery, or other reputation marks and to produce a concise recommendation about whether to answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried phone numbers and a persistent device identifier are sent to a third-party service over unencrypted HTTP.

Mitigation: Use only when users accept that privacy and integrity exposure; prefer a version configured for HTTPS with clear third-party data handling disclosure.

Risk: The backend URL can be changed by environment variable.

Mitigation: Review and pin endpoint configuration before deployment, and restrict environment overrides in managed runtimes.

Risk: The skill stores a persistent UID and daily usage state on the local machine.

Mitigation: Disclose the local state behavior and delete or rotate the state file when resetting the device identity is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengshukaihua/skills/phone-mark-query)
- [Publisher profile](https://clawhub.ai/user/fengshukaihua)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or JSON query reports; documentation includes Markdown with bash command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include the queried number, query time, platform hit count, per-platform marks, risk level, advice, usage count, and a shortened persistent device UID.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
