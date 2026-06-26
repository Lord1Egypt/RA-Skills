## Description: <br>
Calls a Google web search API through a bundled Python helper to fetch search results with titles, links, snippets, and status output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to run a live web search query and summarize returned search results. It supports free-tier use and optional paid authentication through AZT_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and the optional API key are sent to coze-js-api.devtool.uk. <br>
Mitigation: Avoid private or regulated search terms, use a provider-specific key, and install only when this third-party data flow is acceptable. <br>
Risk: Passing the paid key as a command-line argument can expose it through shell history or local process inspection. <br>
Mitigation: Prefer the AZT_API_KEY environment variable and rotate the key if it may have been exposed. <br>
Risk: The helper requires the Python requests dependency. <br>
Mitigation: Install dependencies from trusted package sources in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyriswu/google-search-web) <br>
- [Google search API endpoint](https://coze-js-api.devtool.uk/google/search/web) <br>
- [Devtool plugin page](https://devtool.uk/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown search-result summary, with optional raw JSON output from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, link, snippet, request status, and provider messages when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
