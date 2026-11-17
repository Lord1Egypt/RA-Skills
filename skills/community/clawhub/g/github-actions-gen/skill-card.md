## Description:

Generate GitHub Actions workflow YAML files for CI/CD. Use when setting up automated pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, template, lint, optimize, and inspect GitHub Actions workflow YAML for CI/CD setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The secrets command can expose local lines that look like secrets.

Mitigation: Avoid running the secrets command on sensitive workspaces until argument handling, file validation, and output warnings are fixed.

Risk: File-scanning behavior may mishandle paths or option-like filenames.

Mitigation: Quote file paths, pass -- before filenames, and validate regular files before scanning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/github-actions-gen)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GitHub Actions workflow YAML and related CI/CD review guidance.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
