## Description:

Calls the Jiuwu agent API to analyze text or uploaded files for contract, requirements, and document reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[05u](https://clawhub.ai/user/05u)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and review teams use this skill to send selected text or supported document files to a Jiuwu agent for contract review, requirements review, and document analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tokens and confidential document content may be sent to a hardcoded plaintext HTTP endpoint.

Mitigation: Use the skill only on the intended internal network, require an HTTPS endpoint before confidential use, and confirm the destination is approved.

Risk: Text analysis sends document content in URL query strings.

Mitigation: Avoid sending sensitive text through query strings and prefer a reviewed transport pattern before processing confidential contracts or business documents.

Risk: Dependency ranges are not pinned.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/05u/skills/jiuwu-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful calls return success status and reviewOpinion text; failures return success status false with an error message.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
