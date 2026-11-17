## Description:

Calls a configured LibRAG knowledge-base recall API to retrieve Chinese knowledge-base passages, evidence text, source locations, and structured JSON results for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[7010g](https://clawhub.ai/user/7010g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents working in Chinese knowledge-base workflows use this skill to query a configured LibRAG service, retrieve relevant passages with source text and scores, and support evidence-backed answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Knowledge-base questions and retrieved context are sent to the configured LibRAG endpoint, where an untrusted service or logs could expose sensitive content.

Mitigation: Use a trusted loopback or HTTPS LibRAG endpoint and avoid confidential questions unless the endpoint and its logging are approved for that data.

Risk: The skill requires an API key in configuration, and exposed keys could allow unauthorized knowledge-base recall.

Mitigation: Keep the key private, avoid printing the full key, scope it to the intended knowledge base when possible, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/7010g/skills/librag-knowledge-recall)
- [ClawHub publisher profile](https://clawhub.ai/user/7010g)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON recall results with request details, response payload, and summary fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured LibRAG base URL, API key, knowledge-base ID, recall mode, top-k settings, source text, score, and tree-output options.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
