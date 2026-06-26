## Description: <br>
Provides a technical due diligence screening workflow for assessing technology feasibility, team background, patent claims, business logic, and red-flag risks before technology investment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors, analysts, and due diligence teams use this skill to structure an initial review of technology projects, validate public claims, identify red flags, and draft decision-support reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process confidential deal, company, team, patent, and financial information during due diligence. <br>
Mitigation: Redact personal and commercial details before search, storage, or upload, and require explicit approval before importing or writing back documents. <br>
Risk: The workflow references sensitive IMA API credentials for knowledge-base operations. <br>
Mitigation: Use platform-managed, least-privilege secrets and avoid storing credentials in markdown files, reports, or generated artifacts. <br>
Risk: Generated reports and verifier outputs can make incomplete or weak due diligence appear authoritative. <br>
Mitigation: Treat reports as drafts and independently verify every material claim, source, and investment recommendation before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/golngod/opc-technical-due-diligence) <br>
- [Coze-IMA collaborative due diligence workflow](artifact/references/Coze-IMA协同尽调流程.md) <br>
- [Technology readiness level reference](artifact/references/TRL_levels.md) <br>
- [Technical parameter reference](artifact/references/tech_parameters.md) <br>
- [Scam signal reference](artifact/references/scam_signals.md) <br>
- [Case studies](artifact/references/case_studies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown report drafts, DOCX report files, validation logs, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include due diligence ratings, red-flag lists, source-check notes, investment recommendations, and document-generation outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
