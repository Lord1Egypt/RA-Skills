## Description: <br>
API versioning health auditor that scans REST API source code for unversioned routes, deprecated endpoints missing Sunset headers, hardcoded version strings, inconsistent versioning strategies, and version gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and backend engineers use this skill to audit REST API source code before release for versioning hygiene, deprecation signaling, and framework-specific remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The embedded local scanner reads source files under the selected root, which can include unrelated or sensitive project files if the root is too broad. <br>
Mitigation: Run it against the narrow API project or routes directory that needs auditing rather than a home directory or unrelated monorepo. <br>
Risk: The skill asks the agent to execute local Python analysis code. <br>
Mitigation: Review the skill and scanner behavior before execution, and run it only in workspaces where local source-code scanning is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-api-version-audit) <br>
- [Publisher homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with findings, severity groups, framework-specific fix snippets, and CI fail-gate command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local source-code audit findings and remediation guidance; no external API calls are indicated by the supplied security evidence.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
