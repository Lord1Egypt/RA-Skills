## Description:

Medical Advice helps agents provide Chinese-language symptom analysis, care-seeking guidance, health advice, and optional PubMed/OpenFDA lookups with cited medical and drug-information sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djttt](https://clawhub.ai/user/djttt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure informational medical conversations, identify urgent symptoms, suggest appropriate clinical departments, and retrieve supporting PubMed literature or OpenFDA drug information when relevant. It is not a substitute for professional diagnosis, emergency care, or individualized treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake informational health guidance for diagnosis or emergency medical advice.

Mitigation: Keep the skill's disclaimer visible, avoid definitive diagnoses, and direct severe or persistent symptoms to professional medical care.

Risk: API-backed searches may send medical or drug query terms to NIH/OpenFDA services.

Mitigation: Avoid personally identifying health details in search terms unless the user intentionally wants those terms queried against external services.

Risk: Medical literature and drug data can be incomplete, delayed, or misapplied to an individual case.

Mitigation: Cite PubMed/OpenFDA sources when used and tell users to rely on current clinician guidance for treatment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/djttt/skills/medical-advice)
- [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/)
- [OpenFDA API](https://api.fda.gov/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style Chinese text with optional shell commands and JSON-shaped API result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cited PubMed/OpenFDA links, emergency-care warnings, non-diagnostic disclaimers, and API error messages when network queries fail.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
