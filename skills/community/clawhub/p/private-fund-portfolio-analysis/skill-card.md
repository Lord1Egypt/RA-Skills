## Description: <br>
Helps agents build or revise Python workflows that parse private fund valuation spreadsheets, analyze holdings, hedging, index exposure, sectors, and market-cap distribution, and generate visual portfolio reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoerdata](https://clawhub.ai/user/xiaoerdata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to generate or refine scripts for analyzing private fund valuation XLS/XLSX files, including market-neutral futures hedges and index-enhanced portfolio over/underweight analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill evidence includes real-looking MySQL connection defaults that could cause unintended external database access or expose credentials. <br>
Mitigation: Replace database defaults with nonfunctional placeholders or securely supplied environment variables, and rotate the exposed credential if it may be real. <br>
Risk: Portfolio holdings, generated CSV/JSON/PNG reports, and market-data caches may contain sensitive private fund information. <br>
Mitigation: Run generated analysis in a private workspace, disable external enrichment when holdings must remain local, and delete generated files and caches when no longer needed. <br>


## Reference(s): <br>
- [XLS Structure Reference](references/xls_structure.md) <br>
- [Data Sources Reference](references/data_sources.md) <br>
- [Analysis Script Prompt Generator](scripts/generate_analysis_script_prompt.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of CSV, JSON, and PNG portfolio analysis artifacts.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
