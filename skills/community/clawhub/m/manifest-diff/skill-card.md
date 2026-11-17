## Description:

Diff agent/skill manifests: capabilities, permissions, versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent reviewers, and platform teams use this skill to compare two agent or skill manifests and identify changes in capabilities, permissions, dependencies, versions, and related manifest fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions reference downloading executable Python from a mutable GitHub branch.

Mitigation: Prefer the bundled manifest_diff.py from the reviewed package, or require a pinned commit and checksum before downloading and executing a remote copy.

Risk: The CI verifier executes Python self-tests in target repositories.

Mitigation: Run the verifier only against trusted repositories or inside an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/manifest-diff)
- [Publisher profile](https://clawhub.ai/user/itspremkumar)
- [GitHub repository referenced by artifact](https://github.com/itsPremkumar/manifest-diff)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text summaries or JSON reports from a Python command-line tool, with setup and usage guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares local JSON manifest files and can emit CI-friendly JSON with changed fields, added keys, removed keys, and a summary.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
