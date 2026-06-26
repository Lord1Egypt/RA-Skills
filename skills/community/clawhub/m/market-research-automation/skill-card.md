## Description: <br>
Market Research Automation helps generate market sizing reports, competitor comparisons, and survey questionnaires for product validation using disclosed mock or sample data. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product builders, marketers, and research teams use this skill to draft TAM/SAM/SOM market sizing, competitor comparisons, and user survey questionnaires before product launch or market validation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may rely on mock or sample data and can be mistaken for verified market research. <br>
Mitigation: Treat generated reports as drafts and replace sample data with verified live sources before using the findings for decisions. <br>
Risk: The --output option writes to a user-provided path and may overwrite an intended file. <br>
Mitigation: Use --output only with paths that are safe to create or overwrite. <br>


## Reference(s): <br>
- [Market Research Methodology Reference](references/methodology.md) <br>
- [X/Twitter API](https://developer.x.com/en/docs/x-api) <br>
- [Google Trends](https://www.google.com/trends/) <br>
- [Full Market Research Agent Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/market-research-product-factory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports, survey questionnaires, and console text, optionally written to user-specified files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be treated as drafts; missing data is marked unavailable and current sample data should be replaced with verified sources for real research.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
