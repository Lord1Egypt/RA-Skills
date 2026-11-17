## Description:

Assesses chat conversations and session history for minor, adolescent, student, and school-context indicators, returning a structured JSON risk assessment with evidence and uncertainty notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohanzhang2005](https://clawhub.ai/user/xiaohanzhang2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need a structured, evidence-based assessment of whether a chat participant may be a minor across a single conversation or multiple sessions. It is suited for workflows that require minor-likelihood scoring, student-profile signals, trend analysis, and recommended next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends conversation-derived content and age-profiling signals to configured classifier endpoints.

Mitigation: Use only explicitly trusted endpoints with dedicated low-scope API keys, and avoid this skill for conversations that must remain fully local.

Risk: Logs and observability output may include conversation-derived data or runtime details.

Mitigation: Restrict log access and retention, and review downstream handling of stderr and observability records.

Risk: Retrieval assets can influence evidence and include an unsafe loader path according to the authoritative security summary.

Mitigation: Do not install or replace retrieval asset indexes from untrusted sources; review retrieval assets before enabling embedding-backed retrieval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaohanzhang2005/skills/minor-detection)
- [Output schema](references/output-schema.md)
- [Evidence rules](references/evidence-rules.md)
- [ICBO guidelines](references/icbo-guidelines.md)
- [Classifier system prompt](references/classifier-system.md)
- [Retrieval query template](references/retrieval-query-template.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Single JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes decision, user profile, ICBO features, evidence groups, reasoning summary, trend, uncertainty notes, and recommended next step.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
