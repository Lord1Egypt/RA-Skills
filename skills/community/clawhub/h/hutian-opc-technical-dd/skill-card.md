## Description: <br>
Technical due-diligence screening tool for pre-investment technical feasibility assessment, team background checks, patent verification, business model analysis, and detection of false or exaggerated technology claims. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors, analysts, and due-diligence teams use this skill to screen technology innovation projects before investment by checking source materials, technical feasibility, team and patent claims, business logic, and risk signals. It can produce a structured due-diligence report, red-flag list, risk rating, and investment recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can involve confidential target-company materials and generated due-diligence reports. <br>
Mitigation: Use it only with authorization, understand where uploaded files and reports are stored, keep each client or deal isolated, and prefer read-only or local review for confidential documents. <br>
Risk: The workflow can require IMA API credentials. <br>
Mitigation: Store API keys in managed environment secrets rather than plaintext files, and review credential handling before installation or execution. <br>
Risk: Due-diligence inputs may contain sensitive personal or financial data. <br>
Mitigation: Redact sensitive personal and financial data where possible before processing or uploading materials. <br>


## Reference(s): <br>
- [Coze+IMA Collaborative Due-Diligence Workflow](artifact/references/Coze-IMA协同尽调流程.md) <br>
- [Technology Readiness Levels](artifact/references/TRL_levels.md) <br>
- [Technology Parameters Reference](artifact/references/tech_parameters.md) <br>
- [Scam Signals Reference](artifact/references/scam_signals.md) <br>
- [Case Studies](artifact/references/case_studies.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/golngod/hutian-opc-technical-dd) <br>
- [Publisher Profile](https://clawhub.ai/user/golngod) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured text, generated DOCX files, validation output, and configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include due-diligence findings, red flags, risk ratings, recommendations, and source-verification notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
