## Description:

Helps an agent issue, cancel, and export Sao Paulo municipal service invoices (NFS-e) using local configuration, client records, and certificate-backed SOAP requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackcoffee111](https://clawhub.ai/user/blackcoffee111)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and their agents use this skill to prepare, issue, cancel, and reconcile Sao Paulo NFS-e invoices for local accounting workflows. It is intended for certificate-backed fiscal operations where a human reviews financial details before production actions.

### Deployment Geography for Use:

Brazil (Sao Paulo municipal NFS-e context)

## Known Risks and Mitigations:

Risk: Certificate-backed invoice issuance or cancellation can create real tax effects.

Mitigation: Use non-production data until reviewed, and require explicit human confirmation before every production issuance or cancellation.

Risk: Client, fiscal, and certificate-related data may be retained locally in plaintext.

Mitigation: Store secrets outside tracked files, restrict access to local configuration and client records, and remove temporary certificate material after each run.

Risk: Unsafe XML construction and response logging can expose data or produce malformed fiscal requests.

Mitigation: Fix XML escaping with structured XML generation and disable or redact response logs before production use.

Risk: Invoice links or accounting exports may be sent by email without sufficiently scoped consent.

Mitigation: Require recipient preview and explicit confirmation before sending each invoice link, report, or attachment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blackcoffee111/skills/nota-fiscal-paulistana)
- [Artifact skill behavior](artifact/SKILL.md)
- [Artifact user README](artifact/README.md)
- [Sao Paulo ISS/NFS-e reference file](artifact/ISSSaoPaulo.txt)
- [Sao Paulo NFS-e SOAP endpoint](https://nfews.prefeitura.sp.gov.br/lotenfe.asmx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payloads or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON payloads and accounting exports, and may return official invoice numbers, cancellation status, and PDF links.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version; target metadata matches)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
