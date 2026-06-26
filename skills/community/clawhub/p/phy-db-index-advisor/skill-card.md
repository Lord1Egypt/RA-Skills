## Description: <br>
Database index advisor that statically analyzes ORM query patterns to predict missing indexes, cross-references existing model and migration index definitions, ranks recommendations by query frequency, and outputs CREATE INDEX SQL plus per-ORM migration snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan application source code for ORM query patterns that may need database indexes before deployment. It helps prioritize missing-index recommendations and produce reviewable SQL or ORM migration snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs embedded local Python over a repository path and reads source files during analysis. <br>
Mitigation: Run it only against the intended repository, avoid broad home-directory scans, and review the embedded script before use when local execution risk matters. <br>
Risk: Generated CREATE INDEX SQL or ORM migration snippets may be incomplete or inappropriate for a specific production database workload. <br>
Mitigation: Treat output as recommendations, review with normal database change controls, test in staging, and validate important queries with EXPLAIN ANALYZE before production rollout. <br>
Risk: Static analysis can miss dynamic query construction and may not select optimal composite indexes. <br>
Mitigation: Use higher minimum-count thresholds for noisy projects and manually review columns that frequently appear together in filters, joins, or ordering clauses. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-db-index-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL, ORM migration snippets, shell commands, and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations should be reviewed and validated against the target database before production use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
