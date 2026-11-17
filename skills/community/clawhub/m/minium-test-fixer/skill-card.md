## Description:

Minium Test Fixer helps repair Minium test cases by analyzing error logs and WXML snapshots, identifying better element locators, updating code after confirmation, and verifying the fix with a local test run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiziria](https://clawhub.ai/user/yiziria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to troubleshoot Minium tests that fail because elements cannot be found, locators have gone stale, WXML structure changed, or repeated elements need disambiguation. The workflow supports local logs, cloud test reports, and error screenshots, then proposes a confirmed code fix and requires local validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can run local tests, inspect project files, and edit code after confirmation.

Mitigation: Confirm test runs and file edits before execution, and review proposed locator or Page Object changes before applying them.

Risk: The workflow can manipulate desktop focus when activating WeChat Developer Tools.

Mitigation: Keep unrelated sensitive windows out of focus before running workflows that activate WeChat Developer Tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiziria/skills/minium-test-fixer)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Guidance]

**Output Format:** [Markdown with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed locator changes, file edit guidance, local test commands, and validation results.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
