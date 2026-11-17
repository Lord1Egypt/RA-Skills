## Description:

Medication Safety Advisor helps clinicians, pharmacists, and care coordinators check medication interactions, allergy contraindications, dosing references, and formulary coverage using OpenFDA, RxNorm, and DailyMed while requiring clinician review before prescribing or dispensing decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[optimusprime19](https://clawhub.ai/user/optimusprime19)

### License/Terms of Use:

MIT-0

## Use Case:

External clinicians, pharmacists, and care coordinators use this skill for informational medication-safety checks, including interaction review, allergy contraindication screening, dosing reference lookup, and payer formulary verification. It is not a substitute for licensed clinical judgment or prescribing review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medication-change or dosing guidance may be inaccurate or treated as prescribing advice.

Mitigation: Use the skill only for informational medication-safety support and require review by a licensed clinician or pharmacist before prescribing, dispensing, or changing therapy.

Risk: Drug names, allergy details, or other clinical text sent to public APIs could expose patient-identifying information if users include it.

Mitigation: Submit only drug names and clinical terms; do not send patient identifiers or real patient data unless the deployment satisfies HIPAA requirements and required agreements are in place.

Risk: Formulary coverage may be payer-specific, unavailable, or stale when no real-time formulary integration is configured.

Mitigation: When FORMULARY_API_KEY is not configured, do not estimate tiers or coverage; verify coverage directly with the payer formulary tool or pharmacy benefit line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/optimusprime19/skills/medication-safety-advisor)
- [Project homepage](https://github.com/optimusprime19/medication-safety-advisor)
- [RxNorm drug lookup endpoint](https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name})
- [RxNorm interaction endpoint](https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui={id})
- [OpenFDA drug labeling endpoint](https://api.fda.gov/drug/label.json?search=openfda.brand_name:{name})
- [OpenFDA adverse event endpoint](https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{name})
- [DailyMed structured product labeling endpoint](https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={name})

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Markdown medication-safety reports and reference guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference OpenFDA, RxNorm, DailyMed, and optional formulary API results; recommendations require clinician or pharmacist review.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
