## Description: <br>
AI-driven settlement assistant for parsing natural-language campaign payout rules, confirming the interpreted award pools, and producing local CSV/Excel-based settlement results across equal-split, ranking, hybrid, and weighted modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luxieng030124-max](https://clawhub.ai/user/luxieng030124-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operations teams use this skill to settle creator, sales, or campaign incentive pools from uploaded CSV or Excel data after the agent summarizes the award rules and waits for explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weighted distribution mode may export totals that do not exactly equal the advertised award pool. <br>
Mitigation: Before using results for payouts, verify the CSV summary totals against the intended pool amounts and manually review any weighted-mode settlement. <br>
Risk: Settlement outputs may be treated as payment-ready even when rule interpretation or data-field mapping is ambiguous. <br>
Mitigation: Use the required confirmation step to review every award pool, condition, and total before processing data, and rerun only after discrepancies are corrected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luxieng030124-max/jiesuan) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown/text guidance with Python code blocks, settlement configuration, console summaries, and CSV result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before processing and should include a post-settlement self-check.] <br>

## Skill Version(s): <br>
2.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
