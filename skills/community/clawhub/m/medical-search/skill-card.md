## Description:

Drug safety and medical information search for medication interactions, contraindications, side effects, drug-alcohol and drug-food concerns, and traditional Chinese medicine safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juneyaooo](https://clawhub.ai/user/juneyaooo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search and summarize drug safety information before answering medication-related questions. It is intended for questions about interactions, contraindications, adverse effects, alcohol or food interactions, dosage concerns, and safety for special populations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health queries may be sent to a hard-coded plaintext external search server.

Mitigation: Use only after trusting the server operator and obtaining user consent for external health-query transmission; prefer a trusted HTTPS search provider.

Risk: Shell examples may be unsafe if query parameters are not encoded or handled carefully.

Mitigation: URL-encode query parameters, avoid interpolating untrusted text into shell commands, and review commands before execution.

Risk: Search results may be incomplete, outdated, or unsuitable as definitive medical advice.

Mitigation: Treat results as untrusted references, include source URLs and the medical disclaimer, and direct users to a doctor or pharmacist for clinical decisions.

## Reference(s):

- [Medical Search Skill Page](https://clawhub.ai/juneyaooo/skills/medical-search)
- [Configured SearXNG Medical Search Endpoint](http://43.156.131.167:4000/search?q=QUERY&format=json&language=zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with a direct answer, searched findings, analysis, source URLs, and a medical disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the configured SearXNG search workflow; DDInter lookup is optional when available for Western drug interaction checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
