## Description: <br>
Phy Flag Janitor helps agents scan local source and configuration files for stale, undefined, unused, or hardcoded feature flags and produce a prioritized cleanup report with code locations and confirmation commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit feature-flag debt in a local codebase and plan cleanup work for permanently enabled, permanently disabled, undefined, unused, or test-only flags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local repository contents, which may include sensitive configuration or .env-style files. <br>
Mitigation: Use it only in repositories where the agent is allowed to inspect local files, and avoid sharing generated reports that expose sensitive paths or values. <br>
Risk: Generated cleanup commands and refactor suggestions could remove active flags or code paths if applied without review. <br>
Mitigation: Review matched flags and target files, commit or back up changes first, and run the relevant test suite after applying cleanup changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-flag-janitor) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes local repository files and git history; generated cleanup commands are intended for review before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
