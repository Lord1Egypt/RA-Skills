## Description: <br>
Queries a configured local LibRAG knowledge base for Chinese retrieval, evidence extraction, source text, and source-location recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[7010G](https://clawhub.ai/user/7010G) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to query a configured Chinese LibRAG knowledge base, retrieve relevant passages, and return evidence with request and result metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included config uses a placeholder API key and stores connection settings locally. <br>
Mitigation: Replace the placeholder with a scoped LibRAG key and keep config.json private. <br>
Risk: The skill makes network calls to the configured LibRAG base_url. <br>
Mitigation: Confirm base_url points to the intended LibRAG service before use. <br>
Risk: Retrieved source text may be returned to the agent. <br>
Mitigation: Use only knowledge bases whose retrieved content may be shown in the agent context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/7010G/librag-knowledge-recall) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON returned by the recall script, with command-line usage guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local config.json with LibRAG base_url, api_key, kb_id, recall mode, top-k settings, source-text options, and score filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, created 2026-03-10T07:47:56Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
