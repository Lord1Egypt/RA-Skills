## Description:

AI-powered fertility tracking with personalized temperature pattern detection and multi-signal fusion for ovulation prediction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayi12345](https://clawhub.ai/user/mayi12345)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to track cycle data, combine Oura temperature and HRV data with manually recorded LH, mucus, and symptom signals, and generate ovulation timing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive fertility, symptom, LH, cycle-history, Oura, and partner-contact data.

Mitigation: Store configuration, tokens, current-cycle files, and user-profile files outside shared or backed-up folders and restrict filesystem access to the user running the agent.

Risk: Automatic partner or email alerts may disclose reproductive-health information to another person.

Mitigation: Enable email or partner alerts only after every recipient has explicitly consented and review message destinations before use.

Risk: Ovulation predictions can be mistaken for clinical or contraception guidance.

Mitigation: Treat generated predictions as informational tracking support and consult qualified medical guidance for clinical, fertility-treatment, or contraception decisions.

Risk: Install commands are not pinned to immutable package versions.

Mitigation: Review the package source and lock dependency versions before installing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayi12345/skills/ovulation-tracking)
- [Oura personal access tokens](https://cloud.ouraring.com/personal-access-tokens)
- [Oura Daily Readiness API](https://api.ouraring.com/v2/usercollection/daily_readiness)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ovulation predictions, confidence values, cycle-day status, pattern summaries, and alert guidance from locally stored cycle data.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata and changelog declare 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
