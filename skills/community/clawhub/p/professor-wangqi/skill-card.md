## Description:

Academic learning assistant for Professor Wang Qi's Traditional Chinese Medicine constitution theory, supporting constitution-theory Q&A, clinical-reasoning study, traceable knowledge retrieval, knowledge-base maintenance, and tabular data analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafeng-yan](https://clawhub.ai/user/jiafeng-yan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to study Wang Qi's TCM constitution framework, retrieve evidence-labeled academic or clinical-experience notes, maintain PDF-derived knowledge cards, and analyze constitution-related tables. It is positioned for academic learning and knowledge work, not as a substitute for clinical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional PDF extraction and LLM workflows can send document text and API credentials to a configured endpoint, including plaintext or unexplained endpoints.

Mitigation: Review scripts before use, set an explicit trusted HTTPS or loopback BASE_URL, use a limited API key, and avoid processing confidential or identifiable patient documents.

Risk: Academic and clinical-experience content could be mistaken for diagnosis, prescription, or dosing advice.

Mitigation: Keep outputs framed as academic learning, require evidence labels, avoid individualized diagnosis or dosing, and direct medical decisions to qualified clinicians.

Risk: Installer commands that pipe remote shell scripts can execute unreviewed code.

Mitigation: Avoid curl-to-bash installation paths unless the installer is independently fetched, inspected, and verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiafeng-yan/skills/professor-wangqi)
- [Knowledge card schema](artifact/references/knowledge-card-schema.md)
- [TCM constitution ontology](artifact/references/ontology.md)
- [Future methodology notes](artifact/references/future-methodology.md)
- [Evaluation set](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses, JSON retrieval context, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label evidence level and preserve academic and clinical-safety boundaries.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
