## Description: <br>
Validate and troubleshoot the hybrid database system used by OpenClaw agents (Pulse task DB + RAG Pinecone stack). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptobro-man](https://clawhub.ai/user/cryptobro-man) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to check setup, connection status, and health for an OpenClaw workspace that combines Pulse task database sync with a Pinecone-backed RAG stack. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual environment-variable checks can expose API keys in logs or chat output. <br>
Mitigation: Verify only whether required keys are present and redact secret values from all reports. <br>
Risk: The optional live connectivity test can call OpenAI and Pinecone services from the user's environment. <br>
Mitigation: Ask for confirmation before running live queries and summarize only connection status and redacted errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cryptobro-man/hybrid-db-health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown status summary with PASS/WARN/FAIL labels and next-step bullets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports Pulse DB status, RAG Pinecone status, and exact next fix steps; may include shell commands for local health checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
