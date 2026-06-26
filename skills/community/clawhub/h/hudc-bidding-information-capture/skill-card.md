## Description: <br>
Analyzes SGCC bidding documents in Word, PDF, and Excel formats to extract 23 key fields into a structured Excel report with qualification backfilling and deadline highlighting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jktllsqaq](https://clawhub.ai/user/jktllsqaq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and procurement teams use this skill to run a local analyzer over manually downloaded SGCC tender documents, identify bid-relevant records, and review extracted metadata and keyword matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads tender files from a fixed Desktop folder and writes a report to a fixed Desktop path. <br>
Mitigation: Run it only on intended procurement documents and review the generated workbook before relying on or sharing the results. <br>
Risk: The security scan notes that the script can modify the Python environment by auto-installing dependencies. <br>
Mitigation: Run it in a virtual environment or container and preinstall python-docx, openpyxl, and pdfplumber before execution. <br>
Risk: Tender documents may contain sensitive procurement information. <br>
Mitigation: Review the script before use and avoid running it on sensitive documents outside an approved local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jktllsqaq/hudc-bidding-information-capture) <br>
- [README](artifact/README.md) <br>
- [Sample scenarios](artifact/samples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance plus an Excel report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local tender files from ~/Desktop/sgcc_files and writes ~/Desktop/sgcc_result.xlsx.] <br>

## Skill Version(s): <br>
6.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
