## Description: <br>
Pansxng Websearch provides a self-contained local metasearch workflow based on SearXNG, with commands for search, status, installation, startup, shutdown, engine selection, categories, result counts, language selection, and raw JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local web searches through a SearXNG instance, aggregate results across engines, choose search engines or categories, and fall back to the host agent's built-in web search when the local service cannot return results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A normal search can trigger host setup activity, including installing Homebrew, Python 3.11, Valkey, and SearXNG, cloning code from GitHub, installing Python packages, editing ~/.zshrc, and starting local services. <br>
Mitigation: Review the artifact before installation, run first use in a controlled environment, and treat initial execution as a host setup operation rather than a read-only search query. <br>
Risk: The artifact claims local search privacy, but security evidence warns that privacy should not be relied on without separate routing controls. <br>
Mitigation: Use trusted VPN, proxy, or Tor routing when IP privacy is required, and avoid sending sensitive queries until network routing and SearXNG configuration are independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pansxng-websearch) <br>
- [SearXNG source repository](https://github.com/searxng/searxng) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Formatted search-result text or raw JSON from the local SearXNG API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can include a fallback flag when local search fails; search options include language, result count, engines, and categories.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
