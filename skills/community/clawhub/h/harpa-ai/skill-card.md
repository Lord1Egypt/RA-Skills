## Description: <br>
Automate web browsers, scrape pages, search the web, and run AI prompts on live websites via HARPA AI Grid REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alxsharuk](https://clawhub.ai/user/alxsharuk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call HARPA AI Grid for browser-backed page scraping, web search, and AI prompt or command execution on live websites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through logged-in browser sessions and send page results or AI context to external services. <br>
Mitigation: Use a dedicated browser profile or node with minimal logged-in accounts, approve each target URL and action, and avoid confidential pages. <br>
Risk: Broad node selection and asynchronous webhooks can expand where actions run and where results are delivered. <br>
Mitigation: Select specific nodes, verify webhook destinations before use, and avoid wildcard nodes or long-lived webhooks for sensitive workflows. <br>
Risk: Using page-context prompts can expose full page contents to the selected AI connection. <br>
Mitigation: Use page-context variables only on intended pages and approve the AI connection for the data being processed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alxsharuk/harpa-ai) <br>
- [HARPA Grid web automation](https://harpa.ai/grid/web-automation) <br>
- [HARPA Grid REST API reference](https://harpa.ai/grid/grid-rest-api-reference) <br>
- [HARPA browser automation node setup](https://harpa.ai/grid/browser-automation-node-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HARPA_API_KEY and curl or wget; responses may include scraped page content, search results, or AI command output from HARPA browser nodes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
