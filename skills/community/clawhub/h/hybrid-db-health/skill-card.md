## Description:

Validate and troubleshoot the hybrid database system used by OpenClaw agents (Pulse task DB + RAG Pinecone stack). Use when asked to check setup, connection status, or run a database health test across agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptobro-man](https://clawhub.ai/user/cryptobro-man)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check Pulse database sync and RAG Pinecone connectivity for OpenClaw agent workspaces, then report pass, warning, or failure status with next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented manual fallback can expose OpenAI or Pinecone API keys in logs or chat output.

Mitigation: Use a redacted presence check for required environment variables and rotate any keys that may have been exposed in captured output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptobro-man/skills/hybrid-db-health)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown status report with optional shell commands and next-step bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Pulse DB and RAG Pinecone status as PASS, WARN, or FAIL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
