## Description:

Provides a prioritized reference of MSBuild and dotnet CLI command templates for restoring, building, testing, publishing, packaging, diagnosing, and hardening .NET and ASP.NET workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thecybercore](https://clawhub.ai/user/thecybercore)

### License/Terms of Use:


## Use Case:

Developers and build engineers use this skill to choose practical MSBuild and dotnet CLI commands for common .NET and ASP.NET tasks, including restore, build, test, publish, packaging, diagnostics, and CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MSBuild diagnostics such as binlogs, text logs, and preprocessed project files can expose local project structure, paths, feed URLs, or build metadata.

Mitigation: Review generated diagnostics before sharing them and redact sensitive project or environment details.

Risk: Command templates may include restore sources, private feed authentication, runtime identifiers, output paths, or publish options that are environment-specific.

Mitigation: Treat commands as templates and adjust feed URLs, authentication settings, paths, and publish properties before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thecybercore/skills/msbuild)
- [Publisher profile](https://clawhub.ai/user/thecybercore)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggests the top relevant command templates, key MSBuild properties, and a diagnostic binlog command for failures.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
