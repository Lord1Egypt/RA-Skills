## Description:

Common input handling for Java Maven project review workflows. Use when a Java Maven project arrives as a ZIP archive or a GitLab repository URL and you need to unpack, clone, normalize the project root, and identify Maven modules before deeper review or analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrliugangqiang](https://clawhub.ai/user/mrliugangqiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Java Maven projects from ZIP archives or GitLab repository URLs for downstream review. It normalizes the project root, identifies Maven modules, and produces a standardized project-ingest summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can delete a caller-selected work directory.

Mitigation: Use only disposable temp workspace paths for --work and review the resolved path before execution.

Risk: ZIP archives and repository URLs are untrusted inputs.

Mitigation: Apply size limits, isolate temporary workspaces, use approved GitLab sources, and require explicit user authorization before cloning.

Risk: The script does not enforce all documented GitLab and temp-directory limits.

Mitigation: Have calling workflows validate repository source, SSH authorization, and workspace location before invoking the helper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrliugangqiang/skills/java-maven-common)
- [Publisher profile](https://clawhub.ai/user/mrliugangqiang)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON summary with concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON summary includes input mode, normalized root path, project name, Maven module list, module count, and scan-limitation status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
