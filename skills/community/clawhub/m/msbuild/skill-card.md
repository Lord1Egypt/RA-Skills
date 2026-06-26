## Description: <br>
Provides prioritized MSBuild and dotnet command templates for .NET and ASP.NET restore, build, test, publish, pack, diagnostics, and CI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheCyberCore](https://clawhub.ai/user/TheCyberCore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and build engineers use this skill to choose MSBuild and dotnet CLI command templates for routine .NET and ASP.NET build, test, packaging, publishing, diagnostics, and CI tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested build, clean, publish, restore, or package commands may affect project outputs, dependencies, or release artifacts if run without adapting paths and properties. <br>
Mitigation: Review project paths, output directories, clean or publish actions, restore sources, runtime identifiers, and build properties before allowing an agent to run a suggested command. <br>
Risk: Restore commands that use custom or private package feeds may trigger authentication prompts or access private dependency sources. <br>
Mitigation: Confirm private-feed authentication behavior and feed URLs before execution, especially in shared or automated environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command templates require project-specific paths, output directories, target frameworks, runtime identifiers, restore sources, and authentication settings to be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
