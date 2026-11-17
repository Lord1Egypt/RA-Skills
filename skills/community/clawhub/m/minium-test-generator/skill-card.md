## Description:

Minium recording script to test case tool that helps agents parse recorded scripts and produce project-aligned test cases and page objects while checking step completeness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiziria](https://clawhub.ai/user/yiziria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to convert Minium WeChat mini-program recording scripts into Page Object methods, executable test cases, step comparison tables, and validation reports. It is intended for adding or checking Minium automated tests within a confirmed project workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release may overstate how complete the automatic generator is.

Mitigation: Review generated Page Object methods, tests, and validation reports before relying on them.

Risk: The skill asks for broad project file access and can write files in a test workspace.

Mitigation: Use only a confirmed workspace, require a clear file creation or modification plan, and inspect diffs before applying changes.

Risk: Minium recording scripts can contain tokens, cookies, account data, internal URLs, or other secrets.

Mitigation: Redact sensitive values from recording scripts before sharing them with an agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiziria/skills/minium-test-generator)
- [Artifact README](artifact/README.md)
- [Quick Start Guide](artifact/快速开始.md)
- [Code Generation Quality Control Process](artifact/docs/代码生成质量控制流程.md)
- [Code Review Checklist](artifact/docs/代码审查清单.md)
- [Code Specification](artifact/docs/代码规范.md)
- [Avoid Missing Steps](artifact/core-skills/避免漏掉步骤.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks, plus generated Python test and page object files when used in a workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write files in a user's Minium test workspace after the user confirms the target directory and generation plan.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact frontmatter reports 11.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
