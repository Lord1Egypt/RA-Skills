## Description: <br>
Generate comparative market analysis (CMA) and home valuation reports from IDX listing data and selected comparable properties. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Real estate agents, brokers, and their support teams use this skill to turn subject-property data and selected IDX comparables into CMA reports, valuation ranges, and interactive presentation assets for client review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated interactive HTML can run unsafe listing content when opened or shared. <br>
Mitigation: Review or patch the generated HTML before opening it locally, hosting it, or sending it to clients. <br>
Risk: IDX data and generated CMA files may contain property, location, and valuation details. <br>
Mitigation: Confirm that sharing cma_data.json or hosted reports with Google AI Studio, Gemini Canvas, clients, or other third parties is appropriate for the data involved. <br>
Risk: The CMA output is an estimate for broker or agent support, not a licensed appraisal. <br>
Mitigation: Keep the appraisal boundary visible, disclose assumptions, and review local market nuance, condition differences, concessions, stale comps, and data gaps before using the report for pricing decisions. <br>


## Reference(s): <br>
- [CMA Input Schema](references/cma-input-schema.md) <br>
- [Valuation Guidelines](references/valuation-guidelines.md) <br>
- [Gemini Canvas / AI Studio Publish Checklist](references/gemini-canvas-publish.md) <br>
- [Google AI Studio](https://aistudio.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data, local HTML, and prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cma_report.md, cma_data.json, interactive_local.html, and gemini_canvas_prompt.md from subject and comparable listing JSON inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
