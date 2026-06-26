## Description: <br>
Integrate open construction datasets. Combine open data sources for enhanced analysis <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and construction analytics teams use this skill to combine project data with open construction datasets, including material prices, labor rates, weather, geospatial, permit, energy, and economic data. It supports enrichment, cost-index lookup, weather-risk assessment, structured reporting, and export-oriented analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests filesystem and network access for data integration workflows. <br>
Mitigation: Grant access only to the project files and external data sources needed for the current task, and review any requested exports before sharing sensitive business data. <br>
Risk: External open datasets or provider APIs may return incomplete, stale, or misleading construction data. <br>
Mitigation: Validate inputs, review source metadata and update timing, and treat generated findings as analysis support rather than authoritative construction or financial advice. <br>
Risk: Provider credentials may be needed for some data sources. <br>
Mitigation: Use limited-scope provider keys where possible and provide only the API keys needed for a specific task. <br>


## Reference(s): <br>
- [Open Data Integrator on ClawHub](https://clawhub.ai/datadrivenconstruction/open-data-integrator) <br>
- [datadrivenconstruction Publisher Profile](https://clawhub.ai/user/datadrivenconstruction) <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [OpenWeatherMap API Base URL](https://api.openweathermap.org/data/2.5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with structured tables, summary statistics, key findings, Python examples, and export guidance for Excel, CSV, or JSON when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May present fetched records, enriched project data, cost indices, weather-risk summaries, data availability reports, validation errors, and suggested fixes.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact claw.json states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
