## Description:

Guides cross-platform developers through Chinese and UTF-8 encoding issues on Windows, PowerShell 5.1 mojibake, and common C++20 coroutine pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dqsjqian](https://clawhub.ai/user/dqsjqian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this playbook to troubleshoot Windows encoding, cross-platform build and CI failures, and C++20 coroutine lifetime or scheduling issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Encoding and locale changes can alter console behavior or diagnostic output for a command or session.

Mitigation: Review chcp 65001, PYTHONIOENCODING, and VSLANG=1033 settings before applying snippets; test in the target environment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dqsjqian/skills/platform-pitfalls)
- [Chinese and non-ASCII UTF-8 pipeline](artifact/references/chinese-utf8-pipeline.md)
- [Windows PowerShell 5.1 UTF-8](artifact/references/windows-powershell-utf8.md)
- [C++20 coroutine pitfalls](artifact/references/cpp20-coroutines.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with code and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review suggested changes and verify them on the target Windows environment.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
