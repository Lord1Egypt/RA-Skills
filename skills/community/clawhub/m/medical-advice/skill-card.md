## Description: <br>
Provides symptom-oriented medical information, care-seeking guidance, medication information, and optional PubMed and OpenFDA lookups for cited reference material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Djttt](https://clawhub.ai/user/Djttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to structure symptom questions, understand possible causes, identify when to seek professional or emergency care, and retrieve public medical literature or drug-label information. It is for general medical information and care navigation, not diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat general medical information as a diagnosis or a substitute for professional care. <br>
Mitigation: Present the output as general information only, include a clear non-diagnosis disclaimer, and direct users to professional or emergency care for serious, worsening, or uncertain symptoms. <br>
Risk: API-backed medical or drug searches may include unnecessary personal identifiers if users provide them in queries. <br>
Mitigation: Avoid sending names, contact details, account identifiers, or other unnecessary personal data in PubMed or OpenFDA search terms. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Djttt/medical-advice) <br>
- [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/) <br>
- [OpenFDA API](https://api.fda.gov/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown text with optional JSON-backed PubMed and OpenFDA references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source links, medical disclaimers, and escalation advice for urgent or worsening symptoms.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
