## Description: <br>
GooseWorks is a data toolkit for searching and scraping web, social, people, company, lead generation, and enrichment data through authenticated GooseWorks APIs and runtime skill scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akhilathina](https://clawhub.ai/user/akhilathina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, research, and data operations users can use this skill to find leads, research companies and competitors, scrape supported sites, enrich contacts, and produce structured results through GooseWorks-managed services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch and run remote GooseWorks scripts, which increases execution risk if fetched content is not reviewed. <br>
Mitigation: Review or sandbox fetched scripts before execution and require explicit approval before installing dependencies or running them. <br>
Risk: The skill routes scraping, enrichment, and API proxy tasks through external services that may process personal, proprietary, or paid-call data. <br>
Mitigation: Avoid sending sensitive data unless approved, confirm expected credit cost before paid operations, and follow data handling requirements for downstream providers. <br>
Risk: The GooseWorks API key grants access to account services and credit-backed calls. <br>
Mitigation: Store the key only in the expected local credential file or environment, restrict access, and rotate it if trust changes. <br>


## Reference(s): <br>
- [ClawHub GooseWorks listing](https://clawhub.ai/akhilathina/gooseworks) <br>
- [Publisher profile](https://clawhub.ai/user/akhilathina) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and API examples; downstream task results may include JSON, CSV, or reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOSEWORKS_API_KEY; may fetch runtime scripts and call GooseWorks or proxied third-party APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
