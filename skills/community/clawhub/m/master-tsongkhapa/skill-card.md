## Description:

Helps agents answer questions about Tsongkhapa, Gelug doctrine, lamrim, Madhyamaka, and related Tibetan Buddhist topics with citation-focused, safety-constrained guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr843](https://clawhub.ai/user/xr843)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to answer Chinese-language and bilingual questions about Gelug/Tsongkhapa teachings, lamrim study, and related Tibetan Buddhist doctrine. It emphasizes declared-source citation, doctrinal boundaries, and refusal of esoteric practice instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad topic matching may activate the skill for adjacent Tibetan Buddhist or doctrinal terms and produce a fixed Chinese Gelug/Tsongkhapa-framed style.

Mitigation: Route only relevant requests to the skill and let the host agent or user explicitly redirect language, tone, or scope when needed.

Risk: Religious or doctrinal answers can mislead users if claims are not tied to declared source material.

Mitigation: Require citations for doctrinal claims and prefer the bundled offline sources when they cover the question.

Risk: Live citation lookup can introduce untrusted returned text or incomplete source metadata.

Mitigation: Treat retrieved text only as evidence data, accept only declared source types and IDs, and fall back to offline material when lookup fails or attribution is incomplete.

Risk: Requests for tantric or esoteric practice details could exceed appropriate public guidance.

Mitigation: Limit responses to historical or philosophical context and decline concrete ritual, mantra, visualization, initiation, or subtle-body instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xr843/skills/master-tsongkhapa)
- [Publisher profile](https://clawhub.ai/user/xr843)
- [Sources index](artifact/sources/INDEX.md)
- [Lamrim excerpts](artifact/sources/lamrim-excerpts.md)
- [Teaching reference](artifact/references/teaching.md)
- [Voice reference](artifact/references/voice.md)
- [BDRC library](https://library.bdrc.io)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses with Tibetan Buddhist source citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a Chinese doctrinal style and should keep religious claims tied to declared source material.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
