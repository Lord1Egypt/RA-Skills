## Description: <br>
This skill provides hybrid retrieval (BM25 semantic search + TF-IDF vector similarity) for intelligent template auto-filling. Use when users need to batch fill Word/Excel templates from knowledge bases with high precision matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deweienweide](https://clawhub.ai/user/deweienweide) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to batch fill Word and Excel templates from a structured JSON knowledge base, especially when field names require hybrid BM25 and TF-IDF matching rather than exact keyword lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local template filling can place sensitive or incorrect business data into generated Word and Excel files. <br>
Mitigation: Use copies of templates and knowledge bases, run on one file first, and review generated documents and terminal output before relying on the results. <br>
Risk: Hardcoded paths or placeholder replacement settings can write outputs to the wrong location or replace the wrong company placeholder. <br>
Mitigation: Update the configured knowledge base, template, output paths, and placeholder replacement values before batch execution. <br>


## Reference(s): <br>
- [Quick Start Guide](references/quick_start.md) <br>
- [Algorithm Details](references/algorithms.md) <br>
- [Knowledge Base Format Specification](references/kb_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples; filled Word/Excel files and terminal logs when scripts run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local JSON knowledge bases and template directories; generated documents should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
