## Description: <br>
Runs a traditional Liu Yao divination workflow that generates hexagrams, builds a reading plate, evaluates useful-god relationships, produces plain-language advice, and saves reading history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nycxk](https://clawhub.ai/user/nycxk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to perform and review traditional Chinese Liu Yao readings for questions about work, money, health, study, relationships, and similar topics. Developers and agent operators can run the included script for deterministic or random readings, optionally adding LLM-generated advice when an OpenAI API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal runs save the user's question and generated reading to a local history file. <br>
Mitigation: Use a deliberate --history path and avoid entering sensitive questions unless local history retention is acceptable. <br>
Risk: Enabling --llm sends the question and generated reading context to OpenAI using the user's API key. <br>
Mitigation: Use --llm only when external processing is acceptable, and run without --llm for local rules-based interpretation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nycxk/lingxi-i-ching) <br>
- [Publisher profile](https://clawhub.ai/user/nycxk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, configuration] <br>
**Output Format:** [Console text with structured reading details and local JSONL history records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional LLM interpretation uses OPENAI_API_KEY; default behavior saves each reading to a local history file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
