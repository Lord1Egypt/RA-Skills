## Description: <br>
Visualizes Hermes Agent work with task progress, skill usage, code changes, session statistics, and bilingual reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erich1566](https://clawhub.ai/user/erich1566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Hermes users use this skill to generate visual summaries and reports about agent work, including task progress, tool activity, skill usage, code changes, and session metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may present sample-style values as if they were real Hermes telemetry. <br>
Mitigation: Verify that reports are connected to real telemetry before relying on them for audits, reviews, or operational decisions. <br>
Risk: The monitor stop command may terminate local processes whose command line broadly matches its search pattern. <br>
Mitigation: Review matching processes before stopping the monitor, and run the skill in an isolated environment when process termination could disrupt other work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erich1566/hermes-work-visualization) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/erich1566) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration] <br>
**Output Format:** [Console text plus Markdown, JSON, and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English output with configurable metrics, chart style, report frequency, and export formats.] <br>

## Skill Version(s): <br>
1.1.4 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
