## Description:

Build reusable HTTP API test artifacts from user-provided endpoints, authentication, request data, expected results, and validation rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[may4748854-rgb](https://clawhub.ai/user/may4748854-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert HTTP endpoint details, authentication needs, expected responses, and validation rules into reusable API test files and runnable verification scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe or imported .http definitions can cause the bundled runner to expose environment secrets.

Mitigation: Use only trusted, local API test definitions; run with a minimized environment; prefer non-production or short-lived credentials.

Risk: Generated or imported tests may write responses to unintended writable paths.

Mitigation: Constrain expect.save to a dedicated output directory or remove it when raw response capture is not required.

Risk: Full browser cookies can grant broader access than the test requires.

Mitigation: Avoid full browser cookies when possible and use scoped bearer tokens or short-lived credentials.

## Reference(s):

- [Assertion Cheatsheet](references/assertion-cheatsheet.md)
- [Complex Scenarios](references/complex-scenarios.md)
- [Debugging Cookbook](references/debugging-cookbook.md)
- [HTTP Test Artifact Example](references/http_test_artifact_example.md)
- [ClawHub Skill Page](https://clawhub.ai/may4748854-rgb/skills/http-test)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated .http test files, bash verification scripts, environment templates, and PASS/FAIL/SKIP reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated tests use placeholders for secrets and can read runtime credentials from environment variables.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
