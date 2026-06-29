## Description: <br>
Investor Wiki helps investor-relations teams answer shareholder questions, ingest public disclosure documents into a structured wiki, and run knowledge-base health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gptplusplus](https://clawhub.ai/user/gptplusplus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investor-relations, finance, and communications teams use this skill to maintain a disclosure-backed company wiki and draft cautious, source-cited responses to shareholder or investor questions. It also supports structuring uploaded public disclosure materials and checking wiki health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist uploaded investor-relations documents and question summaries without strong consent or retention controls. <br>
Mitigation: Use only public or approved disclosure materials unless a consent and data-classification step is added; define retention, redaction, or disabling rules for QA logs before use in a real IR workflow. <br>
Risk: Investor-relations answers may be used in regulated external communications where unsupported statements, private information, or stale disclosures could create compliance risk. <br>
Mitigation: Require human IR, legal, or compliance review before external use and keep responses limited to current public disclosures with explicit source citations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gptplusplus/investor-wiki) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Investor knowledge reference index](artifact/references/index.md) <br>
- [Wiki schema and operating rules](artifact/references/wiki/SCHEMA.md) <br>
- [Knowledge-base lint rules](artifact/references/schema/lint_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown answers, structured wiki Markdown and JSON files, and terminal health-check output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [QA mode cites source documents; ingest mode can update wiki pages, source archives, indexes, timelines, and logs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
