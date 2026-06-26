## Description: <br>
MiniMax XLSX Pro helps agents create and validate XLSX, XLSM, and CSV spreadsheet deliverables using Python, LibreOffice recalculation, and MiniMaxXlsx diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and spreadsheet-focused agents use this skill to build publication-ready Excel workbooks, add formulas, charts, and pivots, recalculate formulas, and validate workbook structure before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python, LibreOffice headless, and spreadsheet validation commands. <br>
Mitigation: Use a sandboxed workspace and review generated commands before execution, especially when processing untrusted spreadsheet inputs. <br>
Risk: The recalculation helper may permanently modify the user's LibreOffice macro profile. <br>
Mitigation: Use a disposable LibreOffice profile or back up existing LibreOffice macros before running recalculation. <br>
Risk: The release references a MiniMaxXlsx executable that security guidance says should be verified before invocation. <br>
Mitigation: Confirm the executable exists and is trusted before allowing the skill to run MiniMaxXlsx commands. <br>
Risk: Spreadsheet deliverables can contain incorrect formulas, broken charts, or invalid pivot structures if audit steps are skipped. <br>
Mitigation: Run the documented recalculation, refcheck, chart, and structural checks before delivering workbook files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luaqnyin/minimax-xlsx-pro) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/luaqnyin) <br>
- [Pivot Table Guide](artifact/pivot.md) <br>
- [Chart Guide](artifact/charts.md) <br>
- [Styling Guide](artifact/styling.md) <br>
- [Formula Recalculation Script](artifact/scripts/recalc.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; generated spreadsheet deliverables are XLSX, XLSM, or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local Python, LibreOffice headless, and MiniMaxXlsx validation commands; formula recalculation reports are JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
