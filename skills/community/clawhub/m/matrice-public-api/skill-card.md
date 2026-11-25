## Description:

Integrates the public Matrice del Destino personal and couple matrix endpoints. Use when a task needs to request, explain, or troubleshoot those numerical API results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucernel](https://clawhub.ai/user/lucernel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can request personal or couple numerical matrices from the public Matrice del Destino API, then inspect or troubleshoot the returned results while preserving the documented method identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because a referenced local CLI path could not be resolved.

Mitigation: Check whether the unresolved CLI reference matters for the intended use before installing; use the documented API or configured MCP tool when appropriate.

Risk: Dates of birth are personal data submitted to the public API.

Mitigation: Send only the required date fields, prefer standard input for real dates, and avoid placing dates in URLs, shell history, logs, issues, or telemetry.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lucernel/skills/matrice-public-api)
- [Matrice endpoint reference](references/matrice.md)
- [Personal matrix API](https://matricedeldestino.it/api/public/v1/matrix)
- [Personal matrix method page](https://matricedeldestino.it/calcolo-a-mano)
- [Couple matrix API](https://matricedeldestino.it/api/public/v1/couple)
- [Couple matrix page](https://matricedeldestino.it/matrice-coppia)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON numerical matrix results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves documented version, method, and source fields; results are numerical matrices, not personalized readings.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
