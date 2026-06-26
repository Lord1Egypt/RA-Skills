## Description: <br>
Data pipeline contract enforcer that defines expected schemas at pipeline stage boundaries and validates samples against those contracts to catch schema drift before production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and data engineers use this skill to generate data contracts, validate pipeline outputs, compare old and new samples for schema drift, and produce fix guidance before promoting data between stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may analyze pipeline samples or selected directories that contain unrelated sensitive data. <br>
Mitigation: Limit inputs to the specific sample, contract, or pipeline folder needed for the audit and exclude unrelated sensitive files. <br>
Risk: Generated shell, Python, YAML, or dbt guidance could be incorrect for the user's exact pipeline. <br>
Mitigation: Review generated commands and configuration before running or applying them in development, CI, or production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-pipeline-contract-enforcer) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline YAML, Python, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include contract reports, generated YAML contracts, drift summaries, fix priorities, and dbt test snippets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
