## Description:

Local-first data asset manager that helps agents scan, classify, and report on files before a user decides what data to share.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shangri-la-0428](https://clawhub.ai/user/shangri-la-0428)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inventory local directories, classify individual files, and generate text or JSON reports before sharing or registering selected data assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning broad or sensitive directories can expose more local file inventory information than the user intended to review.

Mitigation: Ask the user to choose a specific scan path, use non-recursive scans for narrow checks when appropriate, and review generated reports before sharing them.

Risk: The skill depends on installing and running an external Python package.

Mitigation: Install only from a trusted datavault package source and avoid running scans with elevated privileges.

Risk: Optional Oasyce registration may share or register information externally.

Mitigation: Treat registration as a separate user-confirmed step after local scan results have been reviewed.

## Reference(s):

- [Oasyce Python Package](https://pypi.org/project/oasyce/)
- [Oasyce Vault on ClawHub](https://clawhub.ai/shangri-la-0428/skills/oasyce-vault)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON report guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide users to produce local scan, classification, and report outputs from selected paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
