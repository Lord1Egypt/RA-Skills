## Description: <br>
Enables an agent to retrieve, create, and analyze Guandata BI datasets, pages, cards, and chart data through a local Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengyuhe123](https://clawhub.ai/user/zhengyuhe123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query Guandata BI, inspect datasets and fields, create report cards, retrieve card data, and analyze BI results from an authorized BI account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Guandata BI credentials stored in local configuration. <br>
Mitigation: Use a least-privilege BI account, keep config.json out of source control, and restrict permissions on the skill directory. <br>
Risk: Returned BI data can be persisted on local disk in cache files. <br>
Mitigation: Avoid highly sensitive datasets unless local caching is acceptable, use task-specific cache separation where appropriate, and clear .cache regularly. <br>
Risk: The skill can create, retrieve, and delete BI pages or cards using the configured account permissions. <br>
Mitigation: Confirm target page and card identifiers before running modifying commands and prefer accounts limited to the intended BI workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhengyuhe123/guandata-bi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, Python code snippets, and CLI text or CSV outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can use config.json for BI connection settings and can persist queried BI data in local CSV or JSON cache files.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
