## Description: <br>
Assistant juridique français RAG sur codes et lois consolidés (LEGI/DILA). Utiliser pour questions de droit français, recherche d'articles, explication de textes législatifs, synthèse juridique avec citations vérifiables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msgnoki](https://clawhub.ai/user/msgnoki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, legal-domain practitioners, and developers use this skill to retrieve French legal code excerpts and prepare citation-grounded answers about French law. It supports general legal information workflows and requires users to treat outputs as non-personalized legal information. <br>

### Deployment Geography for Use: <br>
Global; content scope is French law. <br>

## Known Risks and Mitigations: <br>
Risk: Initial ingestion downloads a large public legal corpus/model and builds local ChromaDB and SQLite indexes, which can consume time, bandwidth, storage, and compute. <br>
Mitigation: Ask for explicit user confirmation before ingestion, run it in a controlled local environment, and use a data directory whose contents can be rebuilt. <br>
Risk: Legal answers may be incomplete or unsuitable for a user's specific facts even when citations are present. <br>
Mitigation: Limit responses to retrieved sources, include the required general-information disclaimer, and direct users to consult a legal professional for personalized advice. <br>


## Reference(s): <br>
- [Answer template](references/answer_template.md) <br>
- [LegalFrance ClawHub release](https://clawhub.ai/msgnoki/legalfrance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON containing retrieved sources, citations, answer structure, and a legal-information disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit search results, RAG prompts, or structured JSON; initial ingestion downloads and indexes the French legal corpus locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
