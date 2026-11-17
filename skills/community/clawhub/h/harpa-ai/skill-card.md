## Description:

Automate web browsers, scrape pages, search the web, and run AI prompts on live websites via HARPA AI Grid REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alxsharuk](https://clawhub.ai/user/alxsharuk)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to call HARPA AI Grid for browser automation tasks such as scraping pages, running web searches, and applying AI prompts to live websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browser page content or AI outputs may be sent to external HARPA Grid or AI services.

Mitigation: Use the skill on public or low-sensitivity pages by default, avoid private or internal account pages unless explicitly approved, and prefer targeted selectors over full-page prompts.

Risk: Webhook delivery can disclose scraped content or AI results to an external endpoint.

Mitigation: Configure resultsWebhook only for endpoints you control and trust, and review what data will be sent before enabling asynchronous delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alxsharuk/skills/harpa-ai)
- [HARPA Grid Web Automation](https://harpa.ai/grid/web-automation)
- [HARPA Grid REST API Reference](https://harpa.ai/grid/grid-rest-api-reference)
- [HARPA Browser Automation Node Setup](https://harpa.ai/grid/browser-automation-node-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HARPA_API_KEY and may operate against browser sessions that are already authenticated to websites.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
