## Description:

Use minimatch for matching file paths with glob patterns like *.js or **/*.ts, supporting advanced glob features and customizable options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need guidance for glob-based file path matching, filtering file lists, generating regular expressions from glob patterns, or configuring minimatch options safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using untrusted user input directly as a minimatch pattern can create regular-expression backtracking risk.

Mitigation: Validate or constrain pattern sources before calling minimatch, and treat the npm package as a normal dependency that should be reviewed for project fit before installation.

## Reference(s):

- [minimatch Optimization Levels](references/optimization.md)
- [ClawHub minimatch skill page](https://clawhub.ai/openlark/skills/minimatch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no hidden execution or persistence behavior found in the security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
