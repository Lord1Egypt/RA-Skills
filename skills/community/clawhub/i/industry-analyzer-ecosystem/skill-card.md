## Description: <br>
Maps an industry's supply-chain ecosystem into upstream, midstream, downstream, and horizontal-support positions with representative companies and a Mermaid diagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Industry analysts, strategy teams, and agents in an industry-analysis workflow use this skill to create a structured ecosystem report for a named industry, including key ecosystem roles, representative companies, barriers, metrics, and information gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or modifies report and session files in the selected output folder. <br>
Mitigation: Run it in the intended project folder and review existing output before rerunning when overwrites matter. <br>
Risk: Industry ecosystem reports can include incomplete or stale company and market data. <br>
Mitigation: Review cited sources and validate representative companies, barriers, and metrics before using the report for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrxparley/industry-analyzer-ecosystem) <br>
- [Ecosystem positions template](references/ecosystem-positions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration] <br>
**Output Format:** [Markdown report with a Mermaid diagram and session JSON updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/{industry-slug}/02-ecosystem.md and updates output/{industry-slug}/session.json.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
