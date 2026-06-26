## Description: <br>
Search Korean patents, utility models, trademarks, and designs via KIPRIS Plus OpenAPI and return normalized JSONL for agents doing prior-art search, competitor monitoring, brand checks, M&A due diligence, and Korean IP analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and IP analysts use this skill to query Korean patent, trademark, design, patent-detail, and applicant records through KIPRIS Plus and receive normalized JSONL for prior-art search, competitor monitoring, brand availability checks, M&A diligence, and Korean IP analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and search terms may be exposed because the default KIPRIS endpoint uses plain HTTP. <br>
Mitigation: Use a low-privilege or quota-limited KIPRIS key, prefer KIPRIS_PLUS_KEY over command-line --key, and set KIPRIS_BASE to an HTTPS endpoint if supported. <br>
Risk: Command-line API key overrides can expose credentials through shell history or process listings. <br>
Mitigation: Provide credentials through the KIPRIS_PLUS_KEY environment variable and avoid passing secrets directly as command arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloepark85/kipris-cli) <br>
- [KIPRIS Plus](https://plus.kipris.or.kr) <br>
- [README](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [JSONL by default, with optional JSON or XML output and Markdown-oriented examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a KIPRIS Plus API key; results depend on KIPRIS Plus availability, quota, rate limits, and query accuracy.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
