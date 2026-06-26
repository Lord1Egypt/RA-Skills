## Description: <br>
Aggregate the 4 dimension outputs (top-enterprise, ecosystem, digital-solutions, opportunity) into one comprehensive industry analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill as the report-synthesis step in an industry-analysis pipeline, combining four upstream Markdown analyses and session metadata into a final Chinese industry-analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill overwrites or updates the local final report when rerun. <br>
Mitigation: Confirm the intended output folder and review a diff or keep a backup before replacing an existing industry-analysis-report.md. <br>
Risk: A synthesized report can carry forward missing, conflicting, or stale information from upstream analysis files. <br>
Mitigation: Review the final Markdown report, especially noted data gaps and cross-dimension insights, before using it for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrxparley/industry-analyzer-editor) <br>
- [synthesis-template.md](references/synthesis-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Guidance] <br>
**Output Format:** [Markdown report written to a local file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads session.json and four upstream Markdown files, writes industry-analysis-report.md, and updates session status.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
