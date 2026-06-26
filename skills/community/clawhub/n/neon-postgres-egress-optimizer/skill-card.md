## Description: <br>
Diagnose and fix excessive Postgres egress from application query patterns that fetch more database data than they use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrelandgraf](https://clawhub.ai/user/andrelandgraf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate high Neon or Postgres network transfer costs, identify high-egress queries, and apply query, pagination, caching, and aggregation fixes that reduce database-to-application data transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running database setup or diagnostic operations against the wrong production target can affect monitoring history or operational assumptions. <br>
Mitigation: Confirm the database target and get approval before creating extensions, resetting pg_stat_statements, or collecting production diagnostic data. <br>
Risk: Changing selected columns, pagination, joins, caching, or aggregation can alter application response behavior. <br>
Mitigation: Run existing tests, verify API response shapes, and measure pg_stat_statements before and after applying changes. <br>


## Reference(s): <br>
- [Neon Network Transfer Documentation](https://neon.com/docs/introduction/network-transfer.md) <br>
- [Neon Cost Optimization Documentation](https://neon.com/docs/introduction/cost-optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with SQL examples and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; users review and apply suggested database diagnostics and code changes manually.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
