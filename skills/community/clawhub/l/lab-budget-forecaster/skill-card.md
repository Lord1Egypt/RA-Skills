## Description: <br>
Lab Budget Forecaster helps estimate grant or lab budget runway from budget, date, and expense inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, lab managers, and agents supporting grant administration use this skill to estimate remaining budget, monthly burn rate, and depletion timing from lab budget and expense inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation and actual command-line arguments differ, which can cause failed or misleading runs. <br>
Mitigation: Check `python scripts/main.py --help` and use the implemented `--budget`, `--start`, `--end`, and `--expenses` arguments before relying on output. <br>
Risk: Budget balances and expense CSVs may contain sensitive lab or grant planning data. <br>
Mitigation: Run the skill locally with only intended budget inputs, avoid unnecessary sensitive fields, and review generated output before sharing. <br>
Risk: Forecasts are simple burn-rate estimates and archived evaluation evidence notes weaker consistency for stress and boundary cases. <br>
Mitigation: Treat results as planning aids, verify assumptions against source records, and manually review edge cases before funding or staffing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/lab-budget-forecaster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and plain-text budget forecast output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read an expense CSV and print a local budget forecast; no network use is indicated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
