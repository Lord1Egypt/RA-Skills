## Description: <br>
Grazer helps agents discover, filter, and engage with content across social, academic, decentralized, media, and agent-network platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottcjn](https://clawhub.ai/user/scottcjn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Grazer to browse, rank, and summarize cross-platform content, then optionally post, comment, cross-post, or generate SVG media through configured service credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured credentials can allow an agent to post publicly or modify account-facing content across multiple services. <br>
Mitigation: Use least-privilege service accounts or tokens, keep credentials in local config, review scopes before use, and rotate tokens after testing or automation changes. <br>
Risk: Automated posting or commenting can create duplicate or unintended public content. <br>
Mitigation: Use dry-run previews and idempotency keys for write commands, especially in scheduled or retrying workflows. <br>
Risk: LLM-based SVG generation can send prompts to a configured OpenAI-compatible endpoint, including plain HTTP if the operator configures one. <br>
Mitigation: Prefer template generation or trusted HTTPS endpoints, and do not send secrets or sensitive prompts to plain-HTTP LLM services. <br>
Risk: Outbound telemetry or tracking-related calls may disclose usage patterns. <br>
Mitigation: Review telemetry, download tracking, and SEO-related calls before enabling automation in sensitive environments. <br>
Risk: The authoritative security verdict is suspicious because broad account actions and outbound features could expose prompts or tokens. <br>
Mitigation: Install only when the operator accepts these cross-service risks, and review the skill and scan evidence before deployment. <br>


## Reference(s): <br>
- [ClawHub Grazer listing](https://clawhub.ai/scottcjn/grazer) <br>
- [BoTTube Grazer skill page](https://bottube.ai/skills/grazer) <br>
- [NPM grazer-skill package](https://npmjs.com/package/grazer-skill) <br>
- [PyPI grazer-skill package](https://pypi.org/project/grazer-skill/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples, Python and JavaScript snippets, JSON configuration examples, text discovery results, and optional SVG markup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write actions depend on locally configured credentials; dry-run previews and idempotency keys are available for supported outbound post and comment commands.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata, package.json, setup.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
