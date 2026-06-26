## Description: <br>
In-depth, multi-region pharmaceutical intelligence search and synthesis, plus drug repurposing, target discovery, clinical evidence review, and bioactivity analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharmaceutical intelligence users, biomedical researchers, and developers use this skill to gather source-grounded regulatory, clinical, literature, target, genetic association, and compound bioactivity evidence across major markets and public biomedical databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad outbound web requests while collecting biomedical and regulatory evidence. <br>
Mitigation: Run it in a constrained workspace and review requested sources before execution. <br>
Risk: Some bundled scripts can save raw API responses to local paths. <br>
Mitigation: Keep raw saving disabled unless needed and write raw outputs only to a dedicated safe directory. <br>
Risk: Untrusted JSON inputs may influence script requests or output paths. <br>
Mitigation: Avoid passing untrusted JSON inputs to the bundled scripts. <br>


## Reference(s): <br>
- [Pharma Intelligence Workflow](references/pharma-intelligence-workflow.md) <br>
- [Sources by Region](references/sources-by-region.md) <br>
- [Sub-Skills Quick Reference](references/sub-skills.md) <br>
- [Drug Naming Conventions by Region](references/drug-naming.md) <br>
- [Regulatory Timelines by Agency](references/regulatory-timelines.md) <br>
- [GEO Within Entrez](skills/ncbi-entrez-skill/references/geo.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, citations, JSON request examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite source tier and access date; bundled scripts may return compact JSON summaries or save raw API responses when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
