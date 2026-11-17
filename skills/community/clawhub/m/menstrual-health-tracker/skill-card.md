## Description:

Tracks menstrual and reproductive health data, analyzes cycles and symptoms across life stages, and produces bilingual guidance plus optional HTML dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web-seeker](https://clawhub.ai/user/web-seeker)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to record menstrual and reproductive-health information, analyze cycle regularity, symptoms, mood, predictions, and life-stage-specific patterns, and generate empathetic health guidance or local dashboard files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive menstrual and reproductive-health records stored in local plaintext files.

Mitigation: Use it only on a private device, keep generated files access-restricted, and delete local records when they are no longer needed.

Risk: Generated dashboard HTML files can contain personal health data and should not be treated as share-safe exports.

Mitigation: Avoid sharing dashboard HTML files and prefer a version that minimizes exported data and writes files with restrictive permissions.

Risk: Dashboard data embedding and imported notes or records may be unsafe until escaping and embedding protections are strengthened.

Mitigation: Avoid importing untrusted records or notes and prefer a version that safely embeds JSON and vendors Chart.js locally.

Risk: Health guidance could be mistaken for diagnosis or clinical advice.

Mitigation: Treat outputs as wellness references and consult a clinician for abnormal symptoms, pregnancy or postpartum concerns, or other medical questions.

## Reference(s):

- [README](artifact/README.md)
- [User Profile System](artifact/references-en/user_profile.md)
- [Multi-Life-Stage Adaptation Logic](artifact/references-en/life_stages.md)
- [Data Analysis Dimensions and Algorithm Reference](artifact/references-en/analysis_engine.md)
- [Empathetic Interaction Guide](artifact/references-en/empathy_guide.md)
- [Menstrual Health Medical Reference Standards](artifact/references-en/medical_standards.md)
- [User Profile System (Chinese)](artifact/references/user_profile.md)
- [Medical Reference Standards (Chinese)](artifact/references/medical_standards.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Plain text or Markdown guidance, local JSON records, and generated HTML dashboard files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local menstrual-health JSON records and export dashboards containing sensitive personal health data.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
