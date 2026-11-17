## Description:

A mathematics calculation skill that helps an AI assistant evaluate expressions, run batch calculations, compute statistics, perform matrix and number-theory operations, convert units, and manage calculation sessions through the XiaoBenYang service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route math, statistics, unit conversion, matrix, number-theory, and session-based calculation requests from an AI assistant to the XiaoBenYang calculation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends calculation requests to a remote XiaoBenYang API and depends on trust in that service.

Mitigation: Review the service and endpoint before installation, and avoid sending sensitive inputs unless the service is approved for the use case.

Risk: The skill asks for an API key and stores it in a local .env file.

Mitigation: Use a non-production or least-privilege key where possible, protect the local environment file, and rotate the key if it may have been exposed.

Risk: The skill exposes administrative/status tools and destructive session-history actions.

Mitigation: Require explicit confirmation before deleting sessions or clearing history, and review tool scope before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/mathematics)
- [ALinkLab publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries of calculation results and service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before use; service responses are returned as raw JSON for the agent to summarize.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
