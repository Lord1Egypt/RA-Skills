## Description: <br>
Guides agents in searching and filtering Amazon products with Sorftime data across marketplaces, query types, and historical monthly snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers, e-commerce operators, and market researchers use this skill to discover products, compare competitors, inspect category or brand portfolios, and query historical product snapshots across supported Amazon marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amazon product queries, user-derived feedback, and the LinkFox API key may be sent to LinkFox services. <br>
Mitigation: Use only with data approved for LinkFox processing, supervise or disable automatic feedback submission where possible, and avoid confidential prompts or business context. <br>
Risk: Large API responses can be written to local JSON files and may contain sensitive commercial data. <br>
Mitigation: Write response files outside git working trees, inspect only needed fields, and delete persisted files when the task is complete. <br>


## Reference(s): <br>
- [Sorftime Product Search API Reference](artifact/references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-sorftime-product-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON API parameters, shell command examples, and tabular result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist large API responses to local JSON files for later field extraction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
