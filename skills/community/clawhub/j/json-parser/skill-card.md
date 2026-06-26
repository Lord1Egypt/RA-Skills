## Description: <br>
Parse and validate JSON data from construction APIs, IoT sensors, and BIM exports. Transform nested JSON to flat DataFrames. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and construction project teams use this skill to parse, validate, flatten, and summarize JSON data from BIM exports, IoT sensor readings, construction APIs, and direct user input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided filesystem paths for JSON parsing and transformation. <br>
Mitigation: Use specific JSON files intended for processing, and avoid credential files, browser profiles, private documents, or whole directories. <br>
Risk: Invalid or unexpected JSON structures can produce parsing errors or incomplete analysis. <br>
Mitigation: Validate inputs before processing and report parsing or schema errors clearly with suggested fixes. <br>


## Reference(s): <br>
- [DataDrivenConstruction](https://datadrivenconstruction.io) <br>
- [Json Parser on ClawHub](https://clawhub.ai/datadrivenconstruction/json-parser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with structured tables, summary statistics, findings, and Python examples when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May offer export options for Excel, CSV, or JSON when relevant.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
