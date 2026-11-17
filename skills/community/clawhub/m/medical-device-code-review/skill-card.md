## Description:

Reviews medical-device software code for safety, quality, cybersecurity, and IEC 62304/YY/T 0664 and China NMPA compliance concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myjnathan](https://clawhub.ai/user/myjnathan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review software for medical devices, including safety classification, code defects, cybersecurity controls, documentation traceability, and China NMPA compliance readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may appear during ordinary code review requests because its trigger wording is broader than its intended medical-device domain.

Mitigation: Use it only when the reviewed software has a medical-device, patient-safety, or regulated healthcare context.

Risk: Regulatory and safety guidance may be incomplete or unsuitable for submissions or safety decisions without expert review.

Mitigation: Validate outputs with qualified medical-device compliance and safety professionals before using them for regulatory submissions or safety-critical decisions.

## Reference(s):

- [IEC 62304 / YY/T 0664 Summary](references/iec-62304.md)
- [FDA Cybersecurity Guidance Summary](references/fda-cybersecurity.md)
- [OWASP Medical Device Security Checklist](references/owasp-medical.md)
- [China NMPA Medical Device Software Compliance Requirements](references/nmpa-compliance.md)
- [FDA Cybersecurity in Medical Devices](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-system-considerations-and-content-premarket)
- [MITRE CVE Database](https://cve.mitre.org/)
- [CISA Cybersecurity Advisories](https://www.cisa.gov/news-events/cybersecurity-advisories)
- [NMPA](https://www.nmpa.gov.cn)
- [CMDE](https://www.cmde.org.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured review findings with severity sections, file and line references when available, and compliance notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
