## Description:

广州日报/融媒云通用测试助手 helps QA and engineering teams generate test cases, run API and link checks, prepare compatibility plans, write test reports, and draft bug tickets for Guangzhou Daily and Rongmei Cloud workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeeye](https://clawhub.ai/user/freeeye)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, developers, and release teams use this skill to plan and document tests for Rongmei Cloud CMS, Guangzhou Daily mobile apps, H5 pages, mini-programs, and backend APIs. It can produce test cases, test reports, bug-ticket drafts, API check results, URL availability checks, and compatibility guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send credentials, security probes, and load-test traffic to user-supplied URLs.

Mitigation: Use it only in authorized Guangzhou Daily or Rongmei Cloud test environments, avoid production tokens and production write endpoints, and obtain approval before testing third-party or internal URLs.

Risk: The bundled scripts may attempt to install Python dependencies automatically.

Mitigation: Install dependencies manually in an isolated environment and review packages before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freeeye/skills/gz-media-tester)
- [API 接口规范参考](artifact/references/api-reference.md)
- [APP 兼容性测试参考](artifact/references/compatibility.md)
- [广州日报/融媒云测试用例库](artifact/references/test-cases.md)
- [测试报告模板](artifact/references/report-template.md)
- [Bug单模板](artifact/references/bug-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON reports, guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run URL or API checks against user-supplied targets and write optional JSON reports when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
