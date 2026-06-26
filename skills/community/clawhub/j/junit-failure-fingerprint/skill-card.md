## Description: <br>
Cluster JUnit failures into stable fingerprints so CI triage focuses on root causes, not noisy one-off logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to compress noisy JUnit XML failures and errors into stable text or JSON fingerprints for root-cause triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JUnit failure messages and stack traces may contain secrets or sensitive runtime values when included in CI logs or annotations. <br>
Mitigation: Scope JUNIT_GLOB to intended test-result directories and review text or JSON output before uploading or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/junit-failure-fingerprint) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text report or JSON object with summary, fingerprint groups, and per-case records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Controlled by JUNIT_GLOB, TOP_N, OUTPUT_FORMAT, STACK_LINES, and FAIL_ON_FAILURES.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
