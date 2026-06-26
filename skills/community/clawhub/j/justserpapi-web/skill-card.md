## Description: <br>
Fetch raw HTML, rendered HTML, or clean Markdown from public webpages through Just Serp API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch known public webpages as source HTML, rendered HTML, or cleaned Markdown for content extraction, page inspection, scrape preparation, and LLM-ready reading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target webpage URLs and fetched content are sent to Just Serp API. <br>
Mitigation: Use the skill only for public or approved URLs, and avoid confidential, internal-only, signed, tokenized, or personal-data-bearing URLs unless your organization has approved the provider and use case. <br>
Risk: The skill requires a sensitive API key for authenticated Just Serp API requests. <br>
Mitigation: Provide JUST_SERP_API_KEY through the runtime environment and avoid pasting it into chat messages, screenshots, logs, or generated files. <br>


## Reference(s): <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web&utm_content=project_link) <br>
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-web) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches a single requested URL per operation and may return raw HTML, rendered HTML, or cleaned Markdown depending on the selected operation.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
