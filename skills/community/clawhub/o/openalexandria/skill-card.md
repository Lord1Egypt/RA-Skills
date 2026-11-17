## Description:

Query and submit artifacts to the OpenAlexandria federated knowledge protocol (reference node by default).

This skill is ready for commercial/non-commercial use.

## Publisher:

[havneco](https://clawhub.ai/user/havneco)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query OpenAlexandria for cached research entries, inspect feed or entry data, and submit JSON research bundles to a configured OpenAlexandria node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and submitted research bundles can be sent to configurable remote endpoints.

Mitigation: Use only trusted HTTPS OpenAlexandria nodes, review OPENALEXANDRIA_BASE_URL before use, and keep API keys scoped and protected.

Risk: Submitted bundle JSON may contain prompts, credentials, private files, personal data, or confidential research.

Mitigation: Inspect bundle JSON before submitting and remove sensitive content unless the selected node is intended to receive and retain it.

## Reference(s):

- [OpenAlexandria skill page](https://clawhub.ai/havneco/skills/openalexandria)
- [Default OpenAlexandria reference node](https://openalexandria.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from the included CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; submissions and whoami require an OpenAlexandria API key.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
