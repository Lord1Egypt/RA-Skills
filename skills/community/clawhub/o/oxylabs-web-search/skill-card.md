## Description: <br>
Search the web and read web pages with Oxylabs AI Studio, returning search results and optional page text or scraped page content as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oxylabs](https://clawhub.ai/user/oxylabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to search the web, gather current source links, and scrape a specific URL as Markdown through Oxylabs AI Studio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, geo options, and fetched page content are sent to Oxylabs AI Studio under the user's API key. <br>
Mitigation: Avoid secrets, internal-only URLs, personal data, regulated data, or confidential research queries unless sharing them with Oxylabs AI Studio is acceptable. <br>
Risk: The skill requires the OXYLABS_AI_STUDIO_API_KEY credential for API access. <br>
Mitigation: Provide the key through OpenClaw configuration or an environment file with appropriate local access controls, and avoid embedding the credential in prompts or shared command output. <br>


## Reference(s): <br>
- [Oxylabs AI Studio API key](https://aistudio.oxylabs.io/api-key) <br>
- [Oxylabs AI Studio API endpoint](https://api-aistudio.oxylabs.io) <br>
- [ClawHub skill page](https://clawhub.ai/oxylabs/oxylabs-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown text printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output can include titles, URLs, descriptions, and optional page content; scrape output returns one URL as Markdown.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
