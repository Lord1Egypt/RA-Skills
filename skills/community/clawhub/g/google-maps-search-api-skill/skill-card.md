## Description: <br>
This skill helps agents extract structured business listings from Google Maps search results through BrowserAct. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to collect local business listings, addresses, ratings, review counts, price ranges, categories, amenities, and review snippets for lead generation, competitor mapping, market research, and CRM preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Maps search terms, location or business parameters, and BrowserAct API quota usage are sent to BrowserAct. <br>
Mitigation: Use the skill only for searches appropriate to share with BrowserAct, and review competitor, prospect, or sensitive-location searches before running them. <br>
Risk: The BrowserAct API key could be exposed if pasted into shared chats or logs. <br>
Mitigation: Keep BROWSERACT_API_KEY in an environment variable and avoid including the key in prompts, transcripts, or command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/google-maps-search-api-skill) <br>
- [BrowserAct Console](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct Workflow API](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, structured data] <br>
**Output Format:** [Terminal status logs followed by printed business listing results as text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; polls task status and retries failed non-authorization runs once.] <br>

## Skill Version(s): <br>
0.1.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
