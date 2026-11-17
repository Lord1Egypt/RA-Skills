## Description:

Query US hospital price transparency data via the MedRates REST API to search medical procedure prices, compare hospitals, and filter by insurance plan and location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimaosipa](https://clawhub.ai/user/dimaosipa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer US hospital-cost questions, compare hospital price transparency data, and prepare MedRates API calls for procedure, payer, plan, and location-specific searches.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Medical-cost searches may send procedure, insurance, and location details to MedRates.

Mitigation: Use CPT or HCPCS codes, ZIP or city-level location, and only the insurance fields needed for the quote; avoid names, account identifiers, street addresses, and unrelated medical history.

Risk: The skill covers US hospital price transparency data only, so results may omit lower-cost non-hospital providers such as independent imaging centers, ambulatory surgery centers, clinics, or physician offices.

Mitigation: Present MedRates results as hospital-specific pricing and note that non-hospital alternatives may exist for outpatient procedures.

## Reference(s):

- [MedRates.fyi](https://medrates.fyi)
- [MedRates API](https://data.medrates.fyi)
- [ClawHub skill page](https://clawhub.ai/dimaosipa/skills/medrates-fyi)
- [Publisher profile](https://clawhub.ai/user/dimaosipa)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, markdown]

**Output Format:** [Markdown with inline JSON and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MedRates API request parameters, endpoint choices, response interpretation, and links for visual exploration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
