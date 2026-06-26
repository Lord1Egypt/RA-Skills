## Description: <br>
Search e-commerce products via n8n webhook integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haresh-sai06](https://clawhub.ai/user/haresh-sai06) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to search an e-commerce catalog with natural language product queries, including category, price, and sorting preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product search queries are sent to an n8n webhook, which may expose user-entered search terms to the configured workflow. <br>
Mitigation: Install only when the receiving n8n workflow is trusted, configure the actual webhook URL before use, and avoid entering sensitive personal, financial, or business information. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown or text summaries of product search results, with webhook responses parsed into a user-facing format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts product search queries to a configured n8n webhook and returns parsed JSON results or user-facing error guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
