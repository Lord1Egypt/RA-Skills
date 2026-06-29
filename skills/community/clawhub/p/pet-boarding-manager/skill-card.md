## Description: <br>
Manage pet boarding operations including owner and pet profiles, reservations, daily care logs, and billing for dogs, cats, and other pets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherine0325](https://clawhub.ai/user/katherine0325) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet boarding providers, kennels, catteries, and pet hotels use this skill to manage customer and pet records, create reservations, log daily care, and calculate boarding fees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores customer, pet health, reservation, care, and billing records in local JSON files. <br>
Mitigation: Store only necessary details, protect the local data folder with device and user access controls, and define retention and deletion practices for old records. <br>
Risk: Boarding records may include operationally sensitive details such as medications, vaccination status, emergency contacts, taxes, and service charges. <br>
Mitigation: Have staff verify health, medication, pricing, and tax details before confirming reservations, issuing invoices, or relying on care logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/katherine0325/pet-boarding-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown-style operational records, examples, calculations, and care-management guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local JSON file names for owners, pets, reservations, care logs, and billing records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
