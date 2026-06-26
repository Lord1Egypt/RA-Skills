## Description: <br>
Generate professional prior authorization request letters for insurance companies with proper clinical justification and formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare operations staff, clinicians, and authorized support teams use this skill to draft prior authorization request letters from patient, provider, service, diagnosis, and clinical justification inputs. It helps produce consistent letters for procedures, medications, durable medical equipment, and imaging requests that still require review by qualified staff before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles patient health information and generated letters may contain sensitive identifiers or clinical details. <br>
Mitigation: Use the minimum necessary patient information, keep inputs and outputs in approved secure local locations, and avoid sharing generated files outside authorized workflows. <br>
Risk: Generated medical necessity language may be incomplete, inaccurate, or unsuitable for a specific insurer or patient record. <br>
Mitigation: Require clinician or authorized staff review against the source record, payer requirements, and supporting documentation before submitting any letter. <br>
Risk: Local execution reads JSON inputs and writes output files, so paths and dependencies can affect privacy and reliability. <br>
Mitigation: Run in a controlled workspace, validate input and output paths, and review dependencies before installing or executing the packaged script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/prior-auth-letter-drafter) <br>
- [Clinical Justification Phrases](artifact/references/clinical_phrases.md) <br>
- [Carrier Requirements](artifact/references/carrier_requirements.json) <br>
- [Clinical Guidelines References](artifact/references/guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Formatted prior authorization letter text with agent-facing Markdown guidance and CLI commands when execution is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structured patient, provider, service, diagnosis, insurance carrier, and clinical justification inputs; generated letters should be reviewed before insurer submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
