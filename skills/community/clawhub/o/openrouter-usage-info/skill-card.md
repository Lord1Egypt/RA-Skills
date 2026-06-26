## Description: <br>
Track OpenRouter API spending - credit balance, per-model cost breakdown, and spending projections from OpenClaw session logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lcajigasm](https://clawhub.ai/user/lcajigasm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to check OpenRouter credit balance, analyze model-level costs from local session logs, and estimate remaining spend runway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenRouter API key sources and local OpenClaw session logs to calculate billing. <br>
Mitigation: Install only when the publisher is trusted for that local access, and prefer an environment-scoped OPENROUTER_API_KEY when practical. <br>
Risk: The optional OpenClaw workspace link step may replace an existing skill path named openrouter-usage. <br>
Mitigation: Review the installer before running it and check existing workspace skills before accepting the link prompt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lcajigasm/openrouter-usage-info) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenRouter API](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [CLI text report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include credit balance, per-model costs, token counts, cache statistics, date filters, agent filters, and spending projections.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
