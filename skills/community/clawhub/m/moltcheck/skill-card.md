## Description:

Security scanner for Moltbot skills. Scan GitHub repositories for vulnerabilities before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltcheck](https://clawhub.ai/user/moltcheck)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Moltcheck Skill to scan GitHub repositories and Moltbot skills for security risks before installation, including risk summaries, trust scores, and permission analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository URLs and an optional MoltCheck API key are sent to a third-party service.

Mitigation: Use the skill only when this data sharing is acceptable, and avoid scanning private repositories until the service's data handling and retention policy is clear.

Risk: The documented npx installation path does not pin a package version.

Mitigation: Prefer a reviewed, pinned release or independently verify the npm package and version before installation.

Risk: The skill depends on a third-party API and payment flow for scans beyond the free tier.

Mitigation: Review pricing, credit handling, and payment instructions before relying on paid scanning.

## Reference(s):

- [MoltCheck Website](https://moltcheck.com)
- [MoltCheck API Documentation](https://moltcheck.com/api-docs.md)
- [MoltCheck OpenAPI Specification](https://moltcheck.com/openapi.json)
- [ClawHub Skill Page](https://clawhub.ai/moltcheck/skills/moltcheck)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON responses with scan scores, grades, risk summaries, permission analysis, credit status, or setup instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan results may include report URLs, remaining credits, and payment/setup guidance returned by the MoltCheck API.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
