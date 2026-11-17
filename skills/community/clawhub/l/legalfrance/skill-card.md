## Description:

Assistant juridique francais RAG sur codes et lois consolides (LEGI/DILA) pour questions de droit francais, recherche d'articles, explication de textes legislatifs et synthese juridique avec citations verifiables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msgnoki](https://clawhub.ai/user/msgnoki)

### License/Terms of Use:


## Use Case:

Agents and users working with French legal questions use LegalFrance to retrieve relevant consolidated code provisions, prepare citation-grounded answers, and identify when available sources are insufficient. It supports general legal information workflows, not personalized legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial ingestion downloads a large legal corpus and model and writes local search indexes, which can consume bandwidth, time, and disk space.

Mitigation: Run ingestion only after explicit user confirmation and expect local Chroma and SQLite indexes to be created or rebuilt.

Risk: French legal answers may be incomplete if retrieved sources do not cover the question.

Mitigation: Use only retrieved sources, cite legal assertions, state when sources are insufficient, and include the required general-information disclaimer.

## Reference(s):

- [LegalFrance ClawHub listing](https://clawhub.ai/msgnoki/skills/legalfrance)
- [msgnoki publisher profile](https://clawhub.ai/user/msgnoki)
- [Answer template](references/answer_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown legal-answer structure with source citations; optional structured JSON prompt payloads from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to cite retrieved French legal sources, state when evidence is insufficient, and include a legal-information disclaimer.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
