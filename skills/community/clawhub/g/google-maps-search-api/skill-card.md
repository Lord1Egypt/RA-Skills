## Description: <br>
This skill helps an agent extract structured business data from Google Maps search results through the BrowserAct Google Maps Search API template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to collect business lead data from Google Maps searches, such as names, addresses, ratings, review counts, categories, amenities, and service options. It is suited to agent workflows where the user provides search keywords and optional language, country, and result-count parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Maps search terms and task parameters are sent to BrowserAct. <br>
Mitigation: Review sensitive lead-generation queries before running the skill and only install it if this data sharing is acceptable. <br>
Risk: The BrowserAct API key may consume account credits or be exposed if pasted into chat. <br>
Mitigation: Set BROWSERACT_API_KEY as an environment variable and avoid pasting the key into chat. <br>
Risk: Network or task failures can cause repeated external API calls. <br>
Mitigation: Limit automatic retries to one attempt and do not retry authorization errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/google-maps-search-api) <br>
- [BrowserAct API key console](https://www.browseract.com/reception/integrations) <br>
- [Google Maps target](https://www.google.com/maps) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON-like structured business records printed by a Python script, with Markdown guidance from the agent when configuration or errors need user action.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY and sends search parameters to BrowserAct; non-authorization failures may be retried once.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
