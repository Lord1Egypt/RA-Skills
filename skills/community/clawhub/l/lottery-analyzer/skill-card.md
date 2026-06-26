## Description: <br>
彩票分析助手 analyzes China Double Colour Ball and China Lotto spreadsheet data to produce statistical trends, pattern summaries, and number recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larval-zz](https://clawhub.ai/user/larval-zz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to analyze local SSQ and DLT lottery-history spreadsheets, inspect hot and cold numbers, summarize recent patterns, and generate statistically informed number sets for reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script writes JSON analysis output and may overwrite an existing result file. <br>
Mitigation: Check the output path before running the analyzer and preserve any prior result files that should be retained. <br>
Risk: Lottery recommendations can be mistaken for reliable predictions. <br>
Mitigation: Treat generated numbers as entertainment or statistical reference only; the evidence guidance states that results should not be considered reliable predictions. <br>
Risk: The analyzer reads local CSV or Excel files supplied by the user. <br>
Mitigation: Use intended lottery-history files only and avoid passing unrelated or sensitive spreadsheets to the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/larval-zz/lottery-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; JSON analysis files when the script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local CSV or Excel lottery-history files and can overwrite JSON result files at the configured output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
