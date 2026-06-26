## Description: <br>
A China pension calculator that helps an agent launch a local web UI, collect pension inputs, calculate basic pension, enterprise annuity, personal pension, and retirement savings, and generate a retirement planning report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hikeryangsz-creator](https://clawhub.ai/user/hikeryangsz-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to estimate retirement income under the China pension system, either by guiding a user through a browser form or by calculating from directly supplied inputs. It is intended for planning support and should not be treated as financial, investment, or official social security advice. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles retirement, income, and savings inputs that can be sensitive personal financial data. <br>
Mitigation: Use it only on trusted devices, avoid sharing full financial details in chat unless intended, and delete generated JSON files and local saved data after use. <br>
Risk: The local web server stores and serves pension inputs while it is running and is described by security evidence as under-protected. <br>
Mitigation: Run the server only on trusted networks, stop it after use, and do not use the skill on shared devices or exposed hosts. <br>
Risk: Pension projections depend on user inputs, formulas, and assumptions and may not match official benefits or future policy changes. <br>
Mitigation: Treat generated reports as planning estimates and confirm important decisions with official social security channels or a qualified financial adviser. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hikeryangsz-creator/pension-calculation) <br>
- [Publisher profile](https://clawhub.ai/user/hikeryangsz-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, JSON calculation data, local web UI links, and short command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on user-provided pension, savings, income, age, retirement age, and return-rate assumptions.] <br>

## Skill Version(s): <br>
1.3.0 (source: server evidence, CHANGELOG, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
