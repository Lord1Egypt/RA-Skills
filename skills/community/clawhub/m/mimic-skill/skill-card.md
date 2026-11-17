## Description:

Mimic Skill helps agents generate SQL and Python templates for extracting MIMIC-IV ICU data such as vital signs, labs, diagnoses, and comorbidities from a user-managed PostgreSQL database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongfanbeta](https://clawhub.ai/user/yongfanbeta)

### License/Terms of Use:

MIT

## Use Case:

Developers, data analysts, and clinical researchers use this skill to draft MIMIC-IV data extraction queries and Python snippets for authorized PostgreSQL database instances. It is intended to speed up retrieval of ICU vitals, labs, diagnoses, comorbidities, and common cohort concepts while leaving database access and execution under the user's control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated queries can support broad extraction of sensitive clinical data.

Mitigation: Install only with authorized MIMIC-IV access, avoid broad all-patient extraction, review each query before execution, and store exported results securely.

Risk: Generated Python examples or database snippets can expose credentials if users paste real secrets into shared code.

Mitigation: Use read-only database credentials where possible and avoid hardcoding real passwords in shared scripts, notebooks, or prompts.

Risk: Database optimization suggestions such as CREATE INDEX can modify shared database state.

Mitigation: Treat CREATE INDEX and similar database administration changes as administrator-only operations and review them before use.

## Reference(s):

- [MIMIC-IV Documentation](https://mimic.mit.edu/docs/IV/)
- [MIMIC-IV on PhysioNet](https://physionet.org/content/mimiciv/3.1/)
- [MIMIC-IV ED on PhysioNet](https://physionet.org/content/mimic-iv-ed/2.0/)
- [MIMIC-IV Note on PhysioNet](https://physionet.org/content/mimic-iv-note/2.0/)
- [MIMIC-CXR on PhysioNet](https://physionet.org/content/mimic-cxr/2.1/)
- [MIMIC Code Repository](https://github.com/MIT-LCP/mimic-code)
- [Schema Reference](references/schema.md)
- [Vital Signs Reference](references/vital_signs.md)
- [Laboratory Tests Reference](references/labs.md)
- [Diagnoses Reference](references/diagnoses.md)
- [Common Query Templates](references/common_queries.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are query and script templates for user-run MIMIC-IV PostgreSQL environments; the skill itself does not connect to a database.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
