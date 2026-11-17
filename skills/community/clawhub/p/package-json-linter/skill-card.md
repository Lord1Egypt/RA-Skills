## Description:

Lint and validate package.json files for common mistakes, missing fields, security issues, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check package.json files, Node.js project configuration, and npm package metadata for structural, dependency, security, and best-practice issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text or Markdown reports may display crafted package metadata in a misleading way when linting untrusted repositories.

Mitigation: Prefer JSON output for automation and review text or Markdown reports before relying on them in decisions.

Risk: Recursive directory scans inspect package.json files under the selected project path.

Mitigation: Run the linter only on project directories you intend to inspect.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/package-json-linter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown lint reports with issue counts and rule-level findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output may exit nonzero when errors are found or when strict mode treats warnings as failures.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; STATUS.md lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
