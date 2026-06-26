## Description: <br>
Post-development full-stack verification skill that runs unit, integration, and end-to-end validation with a real-execution-first workflow after development work is complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardo-lb](https://clawhub.ai/user/leonardo-lb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill after implementation, refactoring, or pre-merge work to analyze the target project, design real-execution-focused tests, run quality gates, guide bounded fixes, and produce delivery-readiness evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start services, run migrations, seed data, delete test artifacts, and make network calls while performing verification. <br>
Mitigation: Run it only in isolated test or sandbox environments with disposable resources, and review the Phase 0 environment report before allowing execution phases. <br>
Risk: Using production credentials or production data during real-execution testing could cause unintended access or side effects. <br>
Mitigation: Use only test accounts, test API keys, and environment-variable-sourced test tokens; do not provide production secrets. <br>
Risk: Higher realism levels may touch more local services and external interfaces. <br>
Mitigation: Confirm the selected realism level and downgrade to a lower level when the project or user intent calls for reduced scope. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leonardo-lb/post-dev-verification) <br>
- [Metrics Reference](references/metrics.md) <br>
- [Test Taxonomy](references/test-taxonomy.md) <br>
- [Feedback Report Schema](references/feedback-schema.md) <br>
- [Anti-Patterns Reference](references/anti-patterns.md) <br>
- [Real E2E Templates](references/real-e2e-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON feedback reports, test code, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start and stop test services, run migrations, seed test data, execute native test runners, and generate reusable test scripts when authorized in a sandbox or test environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
