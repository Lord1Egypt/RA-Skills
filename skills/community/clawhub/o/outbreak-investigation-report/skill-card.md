## Description: <br>
Use this skill when a field epidemiologist, EIS officer, communicable-disease nurse, or public-health investigator needs to draft an outbreak-investigation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External public-health investigators, field epidemiologists, communicable-disease nurses, environmental-health specialists, and hospital infection preventionists use this skill to draft structured outbreak-investigation reports for supervising medical epidemiologist review. It organizes case data, environmental observations, lab results, hypotheses, analytical-study planning, control measures, communication plans, limitations, and action items into a draft report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The draft may contain incomplete or incorrect outbreak-investigation conclusions if source data, baselines, laboratory evidence, or analytical measures are wrong or missing. <br>
Mitigation: Require supervising medical epidemiologist or jurisdictional authority review before release; verify case counts, case definitions, baselines, laboratory results, confidence intervals, p-values, and limitations against source records. <br>
Risk: Working drafts may expose personal health information or small-cell demographic details that could identify individuals. <br>
Mitigation: Redact direct identifiers before use, use case IDs throughout, aggregate demographic strata, and suppress or footnote cells with N below 5. <br>
Risk: Drafted control measures or communication content could be mistaken for authorized public-health action. <br>
Mitigation: Keep outputs labeled as drafts, record the authority responsible for each control measure, and route clinician, public, and affected-community communications through the appropriate public-health lead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/outbreak-investigation-report) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown draft report with structured sections, tables, an edit log, and review banner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only public-health report content; uses de-identified case IDs and includes confidentiality and compliance checks.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
