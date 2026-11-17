## Description:

Morgana Mordred Security Sandbox performs local semantic security analysis of prompts and situations using Ollama embeddings, STC scoring, and security-node classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to classify prompts, incident-style questions, and agent interactions by semantic threat posture, STC score, and the most relevant security node. It is suited for local analysis and stress testing of AI-agent security behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyzed prompts may contain incident details or secrets and are sent to a local Ollama service by default.

Mitigation: Redact sensitive prompt content before analysis and use only a trusted local Ollama endpoint approved for the data being analyzed.

Risk: Install steps use unpinned Python dependencies and model pulls.

Mitigation: Pin the Python package and model versions or digests before deployment, and review dependency and model provenance during release approval.

Risk: Gemma analysis should be treated as enabled by default unless the code is changed.

Mitigation: Disable or modify the secondary model analysis path when only embedding-based classification is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/mordred-security-sandbox)
- [Publisher profile](https://clawhub.ai/user/kofna3369)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Terminal text and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an STC score, logic/social/constitutional component scores, top security node, ranked node scores, optional local model risk line, and timing.]

## Skill Version(s):

4.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
