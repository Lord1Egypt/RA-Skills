## Description:

Help non-English-first users hit the right technical answer when docs, memory, configs, skills, and runbooks are stored under English-heavy names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrix-goh](https://clawhub.ai/user/chrix-goh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and assistants use this skill to bridge multilingual or colloquial user wording to the technical terms, artifacts, memories, skills, runbooks, or official docs most likely to contain the answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage memory or local documentation use for retrieval improvement, which can over-preserve private, one-off, or low-value phrasing if applied indiscriminately.

Mitigation: Persist only confirmed reusable mappings and routing improvements that improve future target matching; avoid storing private or one-off language debris.

Risk: Technical pivots or terminology bridges can misroute a request if they replace the user's original wording too aggressively.

Mitigation: Keep the original input available, preserve exact identifiers verbatim, and select the retrieval surface that matches the target class before applying the bridge.

## Reference(s):

- [Query Expansion](references/query-expansion.md)
- [Retrieval Playbooks](references/retrieval-playbooks.md)
- [Learning Loop](references/learning-loop.md)
- [Publication Readiness](references/publication-readiness.md)
- [Project repository](https://github.com/ChriX-Goh/multilingual-semantic-bridge)
- [ClawHub skill page](https://clawhub.ai/chrix-goh/multilingual-semantic-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, tool calls, privileged actions, or hidden runtime behavior are part of the skill package.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
