## Description: <br>
Schema-driven test data factory generator that reads database schemas or model definitions and generates TypeScript, Python, or SQL test data factories with realistic fake data, relationship ordering, constraints, and optional edge-case variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to turn application schemas and model definitions into repeatable test fixtures, seed data, and factory helpers for TypeScript, Python, or SQL test workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated database cleanup helpers may delete records if run against the wrong database. <br>
Mitigation: Review generated files before running them, use isolated test databases, and remove or guard clearTestData/deleteMany cleanup code unless it cannot connect to production or shared data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-test-data-factory) <br>
- [PHY041 publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with generated TypeScript, Python, SQL, and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local test-data artifacts and setup guidance; generated files should be reviewed before execution, especially database cleanup helpers.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
