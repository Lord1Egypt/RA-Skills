## Description: <br>
Automated API testing with Postman collections via Newman CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and QA engineers use this skill to run Postman collections with Newman, configure environments, generate reports, and integrate API tests into CI/CD pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included test runner can execute unintended shell commands if invoked with crafted inputs. <br>
Mitigation: Review before installing or running; remove eval from scripts/run-tests.sh or run Newman directly with trusted, validated arguments. <br>
Risk: API test runs and generated reports can expose credentials, production endpoints, or sensitive response data. <br>
Mitigation: Use scoped test credentials, avoid production unless explicitly intended, and restrict access to reports and CI artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1999AZZAR/newman) <br>
- [Postman Newman CLI Documentation](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/) <br>
- [CI/CD Examples](references/ci-cd-examples.md) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, YAML, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands and configuration snippets for Newman test execution, report generation, security audits, and CI/CD integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
