## Description:

Validates daily market_data.json files for financial-market reports using null, NaN, numeric type, range, directional consistency, dirty-data, completeness, retry, fail-fast, and issue-reporting checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szrw1825](https://clawhub.ai/user/szrw1825)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and financial analysts use this skill to validate generated market_data.json files before downstream market-report workflows consume them. It returns pass or reject status with concrete issue details for data-quality remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation details may be emailed automatically to a fixed recipient.

Mitigation: Disable email alerts or rebuild them to require explicit opt-in, configurable recipients, and redaction before using sensitive JSON files.

Risk: A hard-coded SMTP credential is present in the artifact.

Mitigation: Revoke the embedded credential, remove it from source, and load mail credentials from a secret manager or protected environment variable.

Risk: Validator imports may resolve from paths outside the installed skill.

Mitigation: Use package-relative imports so only the validators bundled with the installed skill are loaded.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szrw1825/skills/market-data-checker)
- [ClawHub publisher profile](https://clawhub.ai/user/szrw1825)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text, Python CheckResult dictionaries, issue lists, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports PASS or FAIL status with validation rule names, affected fields, observed values, and remediation-oriented messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
