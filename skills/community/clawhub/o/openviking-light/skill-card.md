## Description: <br>
OpenViking Light is a lightweight RAG knowledge base for AI agents that uses local BM25 full-text retrieval and MiniMax LLM answer generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[melonbanjing](https://clawhub.ai/user/melonbanjing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add, search, and query a lightweight local knowledge base, with optional MiniMax-generated answers over retrieved content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated answers send retrieved local knowledge to MiniMax for processing. <br>
Mitigation: Use search.py for local-only retrieval, avoid storing secrets or sensitive notes, and configure MINIMAX_API_HOST only to a trusted HTTPS MiniMax endpoint. <br>
Risk: Missing dependencies may be installed at runtime. <br>
Mitigation: Install and pin jieba in the deployment environment before using the skill. <br>
Risk: The skill maintains a persistent local knowledge store. <br>
Mitigation: Review stored content periodically and avoid adding confidential or regulated data unless the deployment environment is approved for it. <br>


## Reference(s): <br>
- [OpenViking Light on ClawHub](https://clawhub.ai/melonbanjing/openviking-light) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [MiniMax API endpoint](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from command-line scripts, with generated answers returned as text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search can run locally; generated answers require MINIMAX_API_KEY and send retrieved context to MiniMax.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
