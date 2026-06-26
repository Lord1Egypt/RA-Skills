## Description: <br>
Orchestrate and validate the full month-end close for a QBO client by reading the client SOP, running close checks, scoring items, proposing journal entries, tracking close progress, and producing a controller-ready Excel workbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting operators, controllers, and finance teams use this skill to run a monthly close workflow for QBO-connected clients, identify unresolved close items, and prepare proposed journal entries for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses QBO financial data and writes generated Excel workbooks and local close-progress files that may contain confidential financial records. <br>
Mitigation: Run it only in a trusted accounting workspace and handle generated workbooks and .cache/month-end-close files as confidential financial records. <br>
Risk: Proposed journal entries may be incomplete or unsuitable for posting without professional review. <br>
Mitigation: Review proposed journal entries, TBD amounts, and close-check failures before acting on or posting any accounting changes. <br>
Risk: Incorrect client selection or an untrusted local pipeline could run checks against the wrong accounting profile. <br>
Mitigation: Verify the local month-end-close.py script, client slug, QBO client profile, and sandbox flag before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/month-end-close) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, Analysis, Configuration] <br>
**Output Format:** [Markdown instructions with bash examples; execution produces an Excel workbook and a local JSON close-progress cache.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, openpyxl, a valid QBO client profile, and an optional client SOP.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
