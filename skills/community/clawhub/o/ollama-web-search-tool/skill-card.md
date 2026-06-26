## Description: <br>
Uses the Ollama Web Search API to search the web and fetch web page content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnydou](https://clawhub.ai/user/sunnydou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run web searches or fetch page content through Ollama's web endpoints from OpenClaw or a shell. It requires an Ollama API key and the curl and python3 command-line tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and requested URLs are sent to Ollama under the user's API key. <br>
Mitigation: Avoid secret-bearing URLs, internal-only links, personal data, regulated content, and confidential prompts. <br>
Risk: Fetched page text is external web content and may be inaccurate, malicious, or prompt-injection content. <br>
Mitigation: Treat fetched content as untrusted input and review it before using it to make decisions or change files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sunnydou/ollama-web-search-tool) <br>
- [Ollama Web Search API](https://docs.ollama.com/capabilities/web-search) <br>
- [Ollama API Keys](https://ollama.com/settings/keys) <br>
- [OpenClaw Slash Commands](https://docs.openclaw.ai/tools/slash-commands) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text with result titles, URLs, summaries, fetched page content, and page links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search returns up to 10 results; fetch prints up to 2,000 characters of page content and up to 10 links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact files report 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
