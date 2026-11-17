## Description:

Converts source materials such as QA sets, transcripts, meeting notes, training materials, long articles, course documents, policies, and manuals into traceable, searchable, updatable structured knowledge assets for RAG and question-answering agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeasonhaitao](https://clawhub.ai/user/jeasonhaitao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge operations teams, and agent builders use this skill to transform authorized source documents into structured JSONL knowledge assets with a generated Markdown review view, source tracking, tags, relationships, conflict states, and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, confidential, or unauthorized source material could be transformed into reusable knowledge assets.

Mitigation: Use the skill only on explicit, authorized inputs and desensitize private or confidential material before processing.

Risk: Generated Markdown review views may be rendered by tools that allow unsafe raw HTML.

Mitigation: Render generated Markdown in a safe viewer with raw HTML disabled.

Risk: Validation scripts check useful consistency properties but do not replace publication review.

Mitigation: Treat the included validator as a helpful check and perform human review before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeasonhaitao/skills/knowledge-asset-craftsman)
- [Knowledge schema reference](references/knowledge-schema.md)
- [Semantic splitting guide](references/conv-semantic-splitting.md)
- [Tag generation rules](references/tag-rules.md)
- [Knowledge block template](assets/knowledge-block-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [JSONL primary data with generated Markdown review views and supporting reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typical deliverables include knowledge_assets.jsonl, knowledge_assets.md, source_manifest.json, tag_dictionary.json, quality_report.md, retrieval_eval.jsonl, version notes, unresolved questions, and downstream integration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
