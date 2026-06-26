## Description: <br>
Perform Google web and image searches, returning ranked web results with titles, snippets, and URLs or image results with country, language, count, and pagination controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call KeyAPI's Google MCP tools for web and image search, cache returned results, and synthesize search intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled runner can use KEYAPI_TOKEN with non-Google tools. <br>
Mitigation: Use only explicit --platform google commands with web_search or image_search; prefer a Google-only runner or allowlist when available. <br>
Risk: Search queries and results may be cached locally. <br>
Mitigation: Avoid sensitive searches when local caching is not acceptable, use --no-cache for fresh uncached calls, and clear .keyapi-cache when needed. <br>
Risk: The runner can load a plaintext .env token file. <br>
Mitigation: Prefer a protected environment variable for KEYAPI_TOKEN, restrict access to any .env file, and remove stored tokens when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lycici/keyapi-google-search) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Google MCP endpoint](https://mcp.keyapi.ai/google/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance plus JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KEYAPI_TOKEN and Node.js; API responses are cached locally unless caching is disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
