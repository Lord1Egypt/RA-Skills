## Description: <br>
Analyzes MySQL EXPLAIN output and slow-query logs to identify performance bottlenecks and suggest index or SQL rewrite improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DBAs, and database engineers use this skill to parse MySQL EXPLAIN output and slow-query logs, identify likely bottlenecks, and produce practical index or SQL rewrite guidance. Recommendations should be reviewed and tested before changes are applied to production databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production slow-query logs can contain secrets, customer data, tenant IDs, hostnames, emails, or sensitive SQL literals. <br>
Mitigation: Redact logs before sharing them with an agent or service, and prefer local analysis for production database evidence. <br>
Risk: Index and SQL rewrite recommendations are heuristic and may degrade performance or change query behavior if applied blindly. <br>
Mitigation: Review each recommendation manually and test with representative data, EXPLAIN output, and rollback plans before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/mysql-slow-query-analyzer-kay) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/shenghoo123-png) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and structured text with SQL, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include heuristic index recommendations, SQL rewrite suggestions, performance scores, scan-efficiency metrics, and slow-query severity labels.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
