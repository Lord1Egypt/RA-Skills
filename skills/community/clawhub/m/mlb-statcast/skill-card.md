## Description: <br>
Query MLB Statcast data via the statcast MCP server for player lookups, expected stats, pitch arsenals, exit velocity, barrel rate, percentile ranks, standings, and related advanced MLB metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanfoglia](https://clawhub.ai/user/evanfoglia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and sports analysts use this skill to answer advanced MLB player, team, and season questions that require Statcast-derived metrics beyond traditional box-score statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on the third-party statcast-mcp package. <br>
Mitigation: Verify the package source before use in sensitive environments and pin an exact reviewed version. <br>
Risk: Long pitch-level Statcast date ranges can be slow and create unnecessary upstream load. <br>
Mitigation: Keep pitch-level date ranges short and prefer batch tools where the skill supports them. <br>
Risk: Loose player-name matching can return multiple candidates or the wrong player role. <br>
Mitigation: Resolve player IDs first and verify active years or full names before making downstream Statcast calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evanfoglia/mlb-statcast) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Baseball Savant and FanGraphs data through statcast-mcp; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
