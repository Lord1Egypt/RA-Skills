## Description: <br>
Screens technology projects before investment by assessing technical feasibility, team background, patent claims, business logic, and risk signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, investors, and operators use this skill to run an initial technical due diligence screen on technology ventures, including feasibility checks, team and patent verification, red-flag detection, and investment risk rating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process confidential business plans, patent files, financial details, team identities, and other sensitive due-diligence materials. <br>
Mitigation: Use scoped and revocable credentials, obtain approval before importing documents, redact sensitive details before external searches, and limit access to the target knowledge base. <br>
Risk: Reports or imported materials may be persisted in IMA without enough clarity about consent, retention, or access scope. <br>
Mitigation: Confirm who can access the knowledge base, how long records are retained, and whether report write-back is approved before using the collaborative workflow. <br>
Risk: Initial screening findings can be incomplete or misleading if source materials are stale, one-sided, or unsupported. <br>
Mitigation: Treat outputs as preliminary due-diligence guidance, require original test reports for critical claims, and verify important conclusions through at least two independent sources. <br>


## Reference(s): <br>
- [Coze+IMA collaborative due diligence workflow](references/Coze-IMA协同尽调流程.md) <br>
- [Technology readiness level guide](references/TRL_levels.md) <br>
- [Technical due diligence case studies](references/case_studies.md) <br>
- [Technology scam signal checklist](references/scam_signals.md) <br>
- [Technical parameter reference tables](references/tech_parameters.md) <br>
- [ClawHub skill page](https://clawhub.ai/golngod/opc-technical-due-diligence-en) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/golngod) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown due diligence report with red-flag checklist, verification status, risk rating, and investment recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source-backed verification labels and requests for original evidence when key claims remain unverified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
