## Description:

Flatten a PDF into a non-interactive safe version by uploading it to the Solutions API, polling until completion, then returning a download URL for the flattened PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossservicesolutions](https://clawhub.ai/user/crossservicesolutions)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to upload PDFs to the Solutions API and receive flattened, non-interactive PDFs for sharing or archival workflows where active PDF features should be reduced.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents are uploaded to the Cross-Service-Solutions API for processing.

Mitigation: Use the skill only for PDFs the user is comfortable sending to that provider, and avoid confidential or regulated documents unless the provider is approved for the use case.

Risk: An unvalidated base URL override could send PDFs and the API key to an unintended server.

Mitigation: Prefer SOLUTIONS_API_KEY, avoid --base-url or SOLUTIONS_BASE_URL unless the exact HTTPS endpoint is trusted, and validate or remove endpoint overrides before deployment.

Risk: The dependency declaration is broad rather than pinned.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossservicesolutions/skills/make-pdf-safe)
- [CrossServiceSolutions publisher profile](https://clawhub.ai/user/crossservicesolutions)
- [Solutions API registration](https://login.cross-service-solutions.com/register)
- [Solutions API endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [Structured JSON containing job status, file name, and download URL; error responses are also JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a download URL for the flattened PDF after polling the remote job.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
