## Description: <br>
Fetch, classify, and summarize papers from multiple sources (arXiv, etc.) with AI-powered multi-language summaries and email delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PigeonDan1](https://clawhub.ai/user/PigeonDan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and agents use Paper Claw to configure research areas, fetch recent papers, classify them, generate multilingual summaries, and prepare digest outputs for review or email delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The submitted package points to missing runtime files and may not include the complete Paper Claw runtime. <br>
Mitigation: Confirm the complete runtime is present before running fetch, scheduling, reset, or email-delivery commands. <br>
Risk: Local configuration writes and recipient-file updates can affect email recipients and digest state. <br>
Mitigation: Review config, recipient, and state file locations before applying presets or recipient changes. <br>
Risk: Email delivery and optional LLM providers require sensitive SMTP and API credentials. <br>
Mitigation: Use test credentials first, prefer dry-run or preview workflows where available, and avoid enabling scheduled sends until recipients and generated content are reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PigeonDan1/paperclaw) <br>
- [arXiv cs.CL recent papers](https://arxiv.org/list/cs.CL/recent) <br>
- [arXiv cs.CV recent papers](https://arxiv.org/list/cs.CV/recent) <br>
- [arXiv cs.LG recent papers](https://arxiv.org/list/cs.LG/recent) <br>
- [arXiv cs.SD recent papers](https://arxiv.org/list/cs.SD/recent) <br>
- [arXiv eess.AS recent papers](https://arxiv.org/list/eess.AS/recent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON data, Python helper calls, shell commands, and email digest content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable arXiv categories, multilingual summaries, recipient configuration, local state, and optional LLM provider API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
