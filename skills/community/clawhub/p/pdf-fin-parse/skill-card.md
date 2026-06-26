## Description: <br>
Parses finance-industry PDF documents such as annual reports, 10-K filings, and prospectuses into structured Markdown and schema-compliant JSON with financial table post-processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcbc](https://clawhub.ai/user/xcbc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to extract structured Markdown and JSON from financial PDFs, especially documents with dense numeric tables, multi-level headers, borderless tables, and cross-page tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive PDFs and extracted financial content may be sent to Volcano LAS, TOS, and configured VLM providers. <br>
Mitigation: Use dedicated low-privilege API keys, a separate TOS bucket, and only process documents whose retention and external-service handling are acceptable. <br>
Risk: Bucket names, object URLs, or related operational details may appear in logs or output metadata. <br>
Mitigation: Review logs and generated outputs before sharing them, and manually delete uploaded TOS objects when they are no longer needed. <br>
Risk: Financial extraction and business-rule validation are best effort and may produce warnings or incorrect normalized values. <br>
Mitigation: Review validation warnings and source page references in the generated JSON before relying on results for financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xcbc/pdf-fin-parse) <br>
- [Publisher profile](https://clawhub.ai/user/xcbc) <br>
- [Command reference](artifact/references/commands.md) <br>
- [API and prompt conventions](artifact/references/api.md) <br>
- [Configuration guide](artifact/references/configuration.md) <br>
- [Output JSON schema](artifact/assets/output_schema.json) <br>
- [Financial terms glossary](artifact/references/finance_terms.md) <br>
- [Financial table patterns](artifact/references/table_patterns.md) <br>
- [FAQ](artifact/references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated Markdown and schema-compliant JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include document metadata, per-page Markdown, extracted tables, normalized numeric values, source page references, and validation warnings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
