## Description: <br>
Use this skill when a pharmacist, MTM provider, pharmacy resident, or APPE student needs to conduct a Comprehensive Medication Review (CMR) for a patient on multiple medications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharmacists, MTM providers, pharmacy residents, and APPE students use this skill to structure a pharmacist-led Comprehensive Medication Review for one patient and draft a CMR packet for licensed-pharmacist verification. It supports reconciliation, drug-therapy problem identification, Beers or STOPP/START screening, dose review, deprescribing planning, a Medication Action Plan, a Personal Medication List, and prescriber SBAR communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce incorrect, outdated, or incomplete clinical recommendations for drug references, interactions, doses, taper plans, or guideline citations. <br>
Mitigation: Treat every output as a draft and have a licensed pharmacist verify drug names, doses, interactions, citations, and recommendations before prescriber communication or any therapy change. <br>
Risk: Medication review inputs may contain patient identifiers or sensitive health information. <br>
Mitigation: Avoid entering unnecessary patient identifiers and keep any needed patient details confined to the active review session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archlab-space/medication-therapy-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft CMR packet with structured tables and SBAR letter sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [All clinical output is draft-only and requires licensed-pharmacist verification before use.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
