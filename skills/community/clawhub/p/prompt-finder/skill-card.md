## Description: <br>
Searches prompts.chat for AI prompt templates by keyword or category and returns ready-to-use prompt text with source metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laolujava](https://clawhub.ai/user/laolujava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI users and developers use this skill to find reusable prompt templates for tasks such as coding, marketing, education, writing, business, design, productivity, and translation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to an external prompt-template service and may reveal sensitive intent or confidential terms. <br>
Mitigation: Do not search for passwords, tokens, private customer data, unreleased product details, or confidential topics; review queries before invoking the skill. <br>
Risk: Returned prompt templates may be unsuitable, outdated, or include unwanted instructions for a user's context. <br>
Mitigation: Review and adapt returned prompt text before using it in production or customer-facing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laolujava/prompt-finder) <br>
- [prompts.chat](https://prompts.chat) <br>
- [awesome-chatgpt-prompts prompt dataset](https://github.com/f/awesome-chatgpt-prompts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON object containing search status, messages, prompt template results, categories, and sponsor metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are capped at 20 items per request and include ready-to-copy prompt templates.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, artifact frontmatter, package.json, and code header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
