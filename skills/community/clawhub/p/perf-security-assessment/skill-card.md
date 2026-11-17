## Description:

Assesses system performance and security requirements and produces advisory reports covering metrics, risks, and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review architecture plans, target performance indicators, and security test cases, then produce performance status summaries and security risk matrices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment results may be incomplete because the skill provides an advisory workflow and does not run tests or scans by itself.

Mitigation: Validate findings with actual performance tests, security scans, and reviewer confirmation before making release or remediation decisions.

Risk: Inputs may include sensitive architecture, credential, or production details.

Mitigation: Provide only the minimum necessary context and avoid sharing secrets or production access unless explicitly required and approved.

Risk: The workflow is written in Chinese, which may reduce reviewer comprehension for teams that do not read Chinese.

Mitigation: Use reviewers who can understand the source language or translate the generated assessment before acting on its recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/golngod/skills/perf-security-assessment)
- [Publisher Profile](https://clawhub.ai/user/golngod)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report templates with performance findings, security risks, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output; the skill does not run tests or scans by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
