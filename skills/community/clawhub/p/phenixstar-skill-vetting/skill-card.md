## Description:

Vet ClawHub skills for security and utility before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phenixstar](https://clawhub.ai/user/phenixstar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review ClawHub skills before installation, combining automated pattern checks with manual review guidance for security and utility decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the scan workflow is under-contained for hostile skill archives.

Mitigation: Run reviews in an isolated private temp directory or disposable container, and avoid scanning untrusted packages from an environment with sensitive files or credentials.

Risk: The workflow handles downloaded skill archives before the user decides whether to install them.

Mitigation: Inspect archive entries before extraction, avoid preserving archive symlinks, and keep extracted contents outside normal workspaces.

Risk: Automated scanner output can miss issues that require judgment.

Mitigation: Perform the documented manual review even when scanner output is clean, including checks for behavior mismatch, undocumented network calls, broad file operations, and hidden instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phenixstar/skills/phenixstar-skill-vetting)
- [Project homepage](https://github.com/PhenixStar/openclaw-skills-collection)
- [Malicious Code Patterns Database](references/patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scanner findings with file and line references when the included Python scanner is run.]

## Skill Version(s):

1.0.0 (source: server release, target metadata, and skill frontmatter; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
