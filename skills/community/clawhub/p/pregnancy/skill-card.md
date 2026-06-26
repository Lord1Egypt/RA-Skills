## Description: <br>
Track pregnancy routines, symptoms, and clinical signals with flexible logs, weekly summaries, and safety-first triage for medical follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to organize pregnancy tracking, journals, warning-sign triage, and prenatal visit preparation while keeping clinician-facing summaries concise. The skill supports organization and escalation cues, not diagnosis, treatment, or replacement of medical care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pregnancy-related health information may be stored in local plaintext files under ~/pregnancy/. <br>
Mitigation: Use request-only activation when privacy matters, enable only needed modules, and confirm planned local writes before creating or changing files. <br>
Risk: Triage output could be mistaken for medical diagnosis or treatment advice. <br>
Mitigation: Treat outputs as organization and escalation support only, and route urgent symptoms, medication changes, or treatment decisions to emergency services or the user's care team. <br>
Risk: Incomplete timestamps, units, or context can reduce the clinical usefulness of summaries. <br>
Mitigation: Require timestamp, unit, and context for tracked entries, ask clarifying questions before saving ambiguous data, and separate observations from interpretation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/pregnancy) <br>
- [Skill homepage](https://clawic.com/skills/pregnancy) <br>
- [Setup guidance](artifact/setup.md) <br>
- [Tracking framework](artifact/tracking-framework.md) <br>
- [Metric catalog](artifact/metric-catalog.md) <br>
- [Data quality rules](artifact/data-quality.md) <br>
- [Triage rules](artifact/triage-rules.md) <br>
- [Visit summary template](artifact/visit-summary-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown notes, structured summaries, and concise triage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local plaintext files under ~/pregnancy/ after user confirmation; no external network requests are disclosed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
