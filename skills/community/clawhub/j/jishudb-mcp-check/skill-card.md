## Description:

Runs explicitly requested smoke checks or all-tools acceptance tests against a configured JishuDB MCP connector and reports observed results and cleanup status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check a configured JishuDB MCP connector, compare available tools with the packaged contract, and receive a Markdown acceptance report. The default is read-only; a separate approval is needed for temporary write tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Testing a connector without authorization could access an unintended JishuDB environment.

Mitigation: Run only against a connector the user has authorized for testing; default to read-only smoke checks.

Risk: All-tools acceptance creates temporary knowledge-base, document, note, and job data.

Mitigation: Get explicit approval for the write-test scope, touch only run-created resources, and report cleanup failures and remaining resources.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bowen-aijishu/skills/jishudb-mcp-check)
- [Publisher-provided skill homepage (not verified import provenance)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/jishudb-mcp-check)
- [Contract baseline](artifact/references/contract-baseline.md)
- [Test cases](artifact/references/test-cases.md)
- [Acceptance report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown acceptance report with observed test results, coverage gaps, and cleanup status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports blocked or skipped checks rather than claiming unobserved results.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
