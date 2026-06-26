## Description: <br>
Run spreadsheet-compatible Four-Square rental analysis for Paragon MLS deals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real estate investors, analysts, and agents use this skill to evaluate Paragon MLS rental deals for cash flow, NOI, DSCR, appreciation, depreciation, ROI, ROE, and IRR. It is intended for deal underwriting and comparison when users can verify or override rents, expenses, financing assumptions, and rehab inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Build and MCP commands may install dependencies or execute local tooling. <br>
Mitigation: Review commands before running them and use accounts, tokens, and environments with the minimum privileges needed. <br>
Risk: Parsed MLS values and model assumptions may be incomplete or unsuitable for serious underwriting. <br>
Mitigation: Verify rents, expenses, taxes, insurance, financing terms, and rehab inputs before relying on outputs for investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earlvanze/paragon-mls-analyze-deal) <br>
- [Publisher profile](https://clawhub.ai/user/earlvanze) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary with a compact comparison table and detailed JSON blocks for each analyzed deal] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the paragon-mls.analyze_deal MCP tool and accepts MLS numbers plus underwriting assumptions and overrides.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
