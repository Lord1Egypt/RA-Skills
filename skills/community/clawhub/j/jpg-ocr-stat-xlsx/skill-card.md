## Description: <br>
Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, visualization, and formula recalculation for .xlsx, .xlsm, .csv, and .tsv files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and spreadsheet-focused agents use this skill to create, edit, analyze, format, and validate spreadsheet workbooks while preserving formulas and existing templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The formula recalculation helper persistently changes the user's LibreOffice macro profile. <br>
Mitigation: Review before installing or running the helper, and understand that the LibreOffice profile change may affect future LibreOffice use. <br>
Risk: Running the recalculation helper on untrusted workbooks can expose the user to spreadsheet or macro-related risk. <br>
Mitigation: Use copies of important spreadsheets and avoid running recalc.py on untrusted workbooks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/jpg-ocr-stat-xlsx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files, Analysis, Configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus generated or modified spreadsheet files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON status summaries from the formula recalculation helper.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
