## Description:

Li ETL Handle helps agents read, write, clean, transform, merge, join, analyze, and convert Excel and CSV data with Node.js-based utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT

## Use Case:

Developers and data-processing agents use this skill to automate spreadsheet ETL workflows over Excel and CSV files, including cleaning, transformation, joins, aggregation, conversion, and batch merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes custom JavaScript execution through executeScript, which is not a hardened sandbox.

Mitigation: Run only reviewed, trusted script functions and use an isolated environment when processing unfamiliar data.

Risk: The security evidence reports known vulnerability concerns in the Excel parser/dependency setup.

Mitigation: Process only trusted Excel or CSV files, prefer a release that upgrades or replaces xlsx, and regenerate the lockfile from HTTPS package sources.

Risk: Spreadsheet rows may contain sensitive information that could be exposed through debugging or logging.

Mitigation: Avoid logging sensitive rows, mask sensitive fields before inspection, and limit logs to the minimum data needed for troubleshooting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/43622283/skills/li-etl-handle)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [Security Audit](artifact/SECURITY_AUDIT.md)
- [Test Report](artifact/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local spreadsheet file reads and writes; spreadsheet contents and logs should be treated as potentially sensitive.]

## Skill Version(s):

1.0.1 (source: server release evidence, package.json, skill.yaml, and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
