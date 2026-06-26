## Description: <br>
Medication Safety Advisor helps clinicians, pharmacists, and care coordinators check medication interactions, allergy contraindications, formulary coverage, and dosing reference information using public medication data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[optimusprime19](https://clawhub.ai/user/optimusprime19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, pharmacists, and care coordinators use this skill to review medication lists for interaction, contraindication, dosing, and formulary questions before clinical verification. It is informational support only and is not a substitute for licensed clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medication-change guidance could be mistaken for prescribing, dispensing, substitution, dose-change, or medication-hold instructions. <br>
Mitigation: Require review by a licensed clinician or pharmacist before any clinical decision is made from the skill output. <br>
Risk: Queries may expose patient identifiers or protected health information to public medication APIs. <br>
Mitigation: Do not enter names, MRNs, dates of birth, addresses, or other PHI; use only medication names, allergy terms, and non-identifying clinical details. <br>
Risk: Formulary, interaction, and dosing data may be incomplete, outdated, or payer-specific. <br>
Mitigation: Treat outputs as prompts for professional verification and confirm coverage or clinical details with authoritative payer, pharmacy, labeling, or institutional sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/optimusprime19/medication-safety-advisor) <br>
- [Publisher profile](https://clawhub.ai/user/optimusprime19) <br>
- [Project homepage](https://github.com/optimusprime19/medication-safety-advisor) <br>
- [RxNorm API](https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}) <br>
- [RxNorm interaction API](https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui={id}) <br>
- [OpenFDA drug labeling API](https://api.fda.gov/drug/label.json?search=openfda.brand_name:{name}) <br>
- [OpenFDA adverse event API](https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{name}) <br>
- [DailyMed SPL API](https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={name}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured clinical safety summaries and reference notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require clinician or pharmacist review before any prescribing, dispensing, substitution, dose-change, or medication-hold decision.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
