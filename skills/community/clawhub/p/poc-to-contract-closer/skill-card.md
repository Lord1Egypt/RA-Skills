## Description: <br>
Closing playbook for converting a successful ToB POC into a contract. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[william202404](https://clawhub.ai/user/william202404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, PM, and technical teams use this skill after a POC is closeable or near acceptance to convert POC evidence into a contract path. It produces a readiness assessment, gap list, one-page recap, customer message, quote action, launch node, and risk list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer, procurement, budget, or deal data entered into the skill may be business-sensitive. <br>
Mitigation: Use appropriate internal handling for customer information and avoid entering data that should not be processed in the local agent session. <br>
Risk: Generated customer messages or closing recommendations could be inaccurate or misaligned with commercial strategy. <br>
Mitigation: Review and approve generated messages, quote actions, and contract-path recommendations before sending or acting on them. <br>
Risk: If the procurement path, closing window, cooling threshold, decision maker, or unresolved P0 issues are missing, the output may correctly mark the deal as not ready rather than advancing to quote. <br>
Mitigation: Treat missing readiness inputs as action items and confirm the buying path before using the plan for customer-facing commercial steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/william202404/poc-to-contract-closer) <br>
- [Publisher profile](https://clawhub.ai/user/william202404) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown closing plan with checklist tables and customer-message draft] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be produced interactively or from CLI arguments; generated content should be reviewed before customer use.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
