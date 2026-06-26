## Description: <br>
Retrieves simple bibliographic metadata for patents from the Zhihuiya patent database using patent IDs or publication numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patent analysts, IP professionals, and agent users use this skill to retrieve structured front-page metadata for known patents, including titles, abstracts, applicants, inventors, dates, classifications, and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers and lookup context are sent to LinkFox/Zhihuiya services. <br>
Mitigation: Avoid sending confidential research context or proprietary bulk lookup lists unless the user trusts the service with that information. <br>
Risk: The skill uses LINKFOXAGENT_API_KEY for authenticated patent lookup requests. <br>
Mitigation: Store the API key in the environment, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>
Risk: The skill may automatically submit feedback and user context to a separate LinkFox feedback endpoint. <br>
Mitigation: Disable or review feedback submission behavior when user comments, intent, or result quality notes should not be shared. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-simple-bibliography) <br>
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, tables, JSON API responses, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one patentId or patentNumber; batches are limited to 100 identifiers per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
