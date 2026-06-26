## Description: <br>
Data analysis and visualization guidance for querying databases, generating reports, automating spreadsheets, and turning raw data into clear, actionable insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business operators use this skill to structure data analysis, define metrics, select visuals, and turn SQL, spreadsheet, BI, or notebook findings into decision-ready recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or over-broad dataset access can occur when applying analysis guidance to real databases, spreadsheets, or reports. <br>
Mitigation: Scope database, spreadsheet, and report access to the task and avoid sharing unnecessary sensitive raw data. <br>
Risk: Analytical outputs can be misleading when sample size, metric definitions, confounding, or data quality are weak. <br>
Mitigation: Define metric contracts before calculating, quantify uncertainty, check robustness, and downgrade or block conclusions when evidence is insufficient. <br>
Risk: Release metadata includes crypto and purchase capability tags, but the artifact does not implement transaction behavior. <br>
Mitigation: Treat those tags as non-behavioral for this version and re-run security review if a future version adds transaction-related behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-data-analysis) <br>
- [Skill homepage](https://clawic.com/skills/data-analysis) <br>
- [Metric Contracts](metric-contracts.md) <br>
- [Chart Selection](chart-selection.md) <br>
- [Decision Briefs](decision-briefs.md) <br>
- [Analytical Pitfalls](pitfalls.md) <br>
- [Analysis Techniques](techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with analytical summaries, decision briefs, metric definitions, chart recommendations, and optional SQL, Python, spreadsheet, or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external requests or persistence by default; outputs should state evidence, confidence, caveats, and recommended next actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
