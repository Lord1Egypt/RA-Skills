## Description: <br>
Wraps the Exa MCP server (mcp.exa.ai) for web search, deep research, and related tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access Exa MCP search, crawling, company research, code context, LinkedIn search, and deep research tools with hardened safety guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External research prompts, searches, and URLs may be sent to the Exa MCP service. <br>
Mitigation: Use the skill only when that external service exposure is acceptable, and avoid submitting confidential or sensitive data unless approved. <br>
Risk: Deep research can be long-running and resource intensive. <br>
Mitigation: Keep the per-request confirmation guardrail enabled before invoking deep_researcher_start. <br>
Risk: Opaque redirects, internal hostnames, and obfuscated URLs can create SSRF exposure during crawling or search. <br>
Mitigation: Validate destination URLs client-side and refuse shortened, internal, or obfuscated targets when they cannot be verified. <br>
Risk: Large crawls or broad enumeration can consume excessive resources or exceed a legitimate scope. <br>
Mitigation: Proceed with single searches or small user-provided batches and ask the user to scope larger crawl requests. <br>
Risk: Research tools could be misused to seek leaked internal documents, trade secrets, or proprietary strategy. <br>
Mitigation: Refuse espionage-oriented requests and limit company research to legitimate public information. <br>


## Reference(s): <br>
- [Exa MCP server](https://mcp.exa.ai/mcp) <br>
- [Faberlens safety evaluation](https://faberlens.ai) <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/mcp-skill-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls] <br>
**Output Format:** [Markdown responses with MCP tool invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send searches, URLs, and research prompts to the external Exa MCP service; deep research requires per-request confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
