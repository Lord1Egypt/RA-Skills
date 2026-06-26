## Description: <br>
Helps pharmacovigilance teams draft ICH E2D / GVP Module VI-aligned Individual Case Safety Report narrative packets, including case-validity checks, reportability clock calculations, and draft-only review labels before submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drug-safety processors, pharmacovigilance scientists, QPPVs, MAH safety teams, and PV vendors use this skill to turn a single adverse-event case into a structured draft ICSR narrative packet for qualified medical and regulatory review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles sensitive pharmacovigilance case information. <br>
Mitigation: Enter only information needed for drafting, avoid unnecessary patient identifiers, and keep source case files under normal privacy controls. <br>
Risk: Draft narratives, reportability clocks, coding proposals, causality, expectedness, or seriousness flags could be mistaken for final regulatory determinations. <br>
Mitigation: Treat all outputs as draft material and require safety-physician, QPPV, and medical-coder review before any regulatory action. <br>
Risk: Source-document wording could expose private information or be copied too directly into the narrative. <br>
Mitigation: Summarize source material, preserve only permitted de-identified case facts, and refuse full patient names, full dates of birth, addresses, national IDs, medical record numbers, insurance IDs, phone numbers, and email addresses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/pharmacovigilance-icsr-narrative) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown narrative packet with tables, follow-up questions, reportability status, and review blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only output; de-identification and qualified safety-physician or QPPV review are required before regulatory action.] <br>

## Skill Version(s): <br>
0.1.1 (source: evidence.release.version and CHANGELOG.md, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
