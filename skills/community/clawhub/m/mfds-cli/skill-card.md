## Description:

A command-line skill for querying Korea Ministry of Food and Drug Safety public APIs for drug permissions, consumer drug information, DUR contraindications, and recall or sale-stop alerts, with normalized JSONL output for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare workflow builders use this skill to retrieve Korean public drug data for pharmacy AI, medication-safety checks, prescription review workflows, supplement diligence, and healthcare data pipelines. It is most useful when an agent needs structured MFDS data rather than manually handling separate XML or JSON endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom endpoint override can send the MFDS API key and medication-related search terms to a non-MFDS destination.

Mitigation: Use the default data.go.kr HTTPS endpoints and allow --endpoint only for destinations that are fully trusted.

Risk: Drug and ingredient search fields can contain sensitive patient-related information.

Mitigation: Do not include patient identifiers or other private patient data in search terms.

Risk: An MFDS API key may be exposed if it was used with an untrusted endpoint.

Mitigation: Rotate the MFDS API key after any use with a non-MFDS or otherwise untrusted endpoint.

## Reference(s):

- [data.go.kr public API portal](https://www.data.go.kr)
- [ClawHub release page](https://clawhub.ai/chloepark85/skills/mfds-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI responses are JSONL by default, with JSON and XML options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MFDS_API_KEY; normalized records retain unmapped source fields under _raw.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
