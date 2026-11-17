## Description:

Parses financial PDF documents, including annual reports, 10-K filings, and prospectuses, into structured Markdown and schema-compliant JSON with financial table post-processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcbc](https://clawhub.ai/user/xcbc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and financial document analysts use this skill to convert finance-heavy PDFs into Markdown and structured JSON tables. It is designed for cross-page tables, borderless tables, multi-level headers, dense numeric values, and business-rule validation warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial PDFs may be uploaded to external LAS and TOS services during parsing.

Mitigation: Review data-handling requirements before use, avoid confidential documents unless approved, and use dedicated least-privilege credentials.

Risk: Uploaded cloud objects may remain available if bucket cleanup is not configured.

Mitigation: Use a dedicated TOS bucket with short lifecycle expiration and review upload retention before processing documents.

Risk: The install flow references dependencies from a parent manifest that is not included and pinned inside the skill package.

Mitigation: Review and pin the dependency manifest before running pip install or deploying the skill.

Risk: Custom API or storage endpoints could route documents to untrusted services.

Mitigation: Use only controlled endpoints and verify LAS/TOS endpoint configuration before running the parser.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xcbc/skills/pdf-fin-parse)
- [Command Reference](references/commands.md)
- [API and Prompt Contract](references/api.md)
- [Configuration Guide](references/configuration.md)
- [Output JSON Schema](assets/output_schema.json)
- [Finance Terms Glossary](references/finance_terms.md)
- [Financial Table Patterns](references/table_patterns.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and file-based Markdown/JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary outputs include output.json, output.md, meta.json, raw LAS response data, per-page Markdown, source-page traces, and validation warnings.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
