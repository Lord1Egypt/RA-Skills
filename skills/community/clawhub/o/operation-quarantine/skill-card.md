## Description: <br>
Prompt injection defense for OpenClaw agents. Scans emails and skill installations through a two-phase security pipeline (pattern matching + optional LLM analysis) before untrusted content enters your context. Use before reading any email body content or installing any skill from ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dank-varley](https://clawhub.ai/user/dank-varley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan untrusted email bodies and skill packages before an OpenClaw agent processes or installs them. It returns clean, suspicious, or blocked verdicts with sanitized content, summaries, flags, and installation recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive email or skill content may be sent to configured LLM providers or custom alert webhooks when optional integrations are enabled. <br>
Mitigation: Use the default local-only mode for sensitive content; enable LLM analysis or custom webhooks only when those privacy tradeoffs are acceptable. <br>
Risk: Exposing the quarantine service beyond localhost can make scan endpoints reachable outside the local agent environment. <br>
Mitigation: Keep the bind host at 127.0.0.1 unless intentionally exposing the service. <br>
Risk: If the quarantine service is unavailable, processing raw content without a scan can bypass the intended protection. <br>
Mitigation: Follow the documented fail-closed behavior: treat scanner errors or unreachable service responses as blocked and do not process raw content. <br>


## Reference(s): <br>
- [ClawHub skill documentation](https://clawhub.ai/skills/operation-quarantine) <br>
- [ClawHub skill page](https://clawhub.ai/dank-varley/operation-quarantine) <br>
- [Signatures README](signatures/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON API responses and Markdown instructions with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Clean verdicts may return sanitized content; suspicious or blocked verdicts withhold raw content and return summaries, flags, or recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence, service/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
