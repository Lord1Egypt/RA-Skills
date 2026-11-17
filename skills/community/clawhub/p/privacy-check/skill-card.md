## Description:

Privacy Check scans local files and directories for common personally identifiable information and sensitive tokens, then reports masked findings in JSON, CSV, HTML, or terminal summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data stewards, and security reviewers use this skill to scan chosen text files or directories for PII before data release, privacy review, compliance preparation, or de-identification work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can mishandle sensitive scan results.

Mitigation: Run scans only on intentionally selected paths, keep reports private, and limit access to generated artifacts.

Risk: Context output can aggregate sensitive data even when masking is intended.

Mitigation: Leave context disabled by default and enable --context only when needed for review.

Risk: HTML reports for untrusted scanned files may expose or execute sensitive content if escaping is incomplete.

Mitigation: Prefer JSON or CSV for untrusted inputs until HTML escaping and context masking are fixed by the publisher.

## Reference(s):

- [Privacy Check ClawHub Page](https://clawhub.ai/cqdev-ai/skills/privacy-check)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands; scanner reports are JSON, CSV, HTML, or terminal text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-selected files; report contents may include masked sensitive findings.]

## Skill Version(s):

1.0.1 (source: server release, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
