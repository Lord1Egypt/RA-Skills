## Description: <br>
Real-time web search for OpenClaw commander agents using local SearXNG, page browsing, claim verification, and optional Gemini Google Search grounding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psanger](https://clawhub.ai/user/psanger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search for current web information, browse result pages, and cross-check factual claims before answering. It is intended for OpenClaw environments that can run shell commands and have trusted search, browsing, or optional Gemini API endpoints configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is framed as local or private, but searches, browsing, fallback services, proxies, browser workers, and optional Gemini grounding can send queries or URLs to configured network endpoints. <br>
Mitigation: Use a SearXNG instance you control, leave LOCAL_SEARCH_FALLBACK_URL and BROWSER_WORKER_URL unset unless those services are trusted, and avoid sensitive searches through unknown proxies. <br>
Risk: Optional Gemini or 1Password access requires sensitive credentials. <br>
Mitigation: Enable Gemini mode only when needed, use a scoped API key for this purpose, and do not print or include secret values in prompts, logs, or outputs. <br>
Risk: Fetched pages and search snippets can be incomplete, blocked, stale, or misleading. <br>
Mitigation: Use full-page browsing and claim verification before asserting factual claims, prefer cross-validated results, and report insufficient evidence when verification is uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/psanger/local-web-search) <br>
- [Scrapling](https://github.com/D4Vinci/Scrapling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown or JSON with search results, page extracts, citations, confidence signals, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source URLs, published dates, fetched page text, grounding metadata, claim-verification verdicts, and confidence scores.] <br>

## Skill Version(s): <br>
4.2.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
