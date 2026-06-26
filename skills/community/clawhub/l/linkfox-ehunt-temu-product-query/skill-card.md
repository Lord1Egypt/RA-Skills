## Description: <br>
Filters and queries Temu product data through LinkFox EHunt by keyword, product or store ID, category, price, ratings, reviews, sales, listing status, fulfillment mode, region, tags, and sorting options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace researchers, product-sourcing teams, and agents use this skill to query Temu products through LinkFox EHunt and compare price, sales, ratings, reviews, categories, fulfillment mode, regions, and listing status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The response_io helper can execute a local Python script path supplied to it. <br>
Mitigation: Use response_io only with the intended scripts/ehunt_temu_product_query.py script and review installation carefully when the agent has broad shell access. <br>
Risk: The skill requires LINKFOXAGENT_API_KEY and sends requests to LinkFox services. <br>
Mitigation: Store the API key in environment variables or secret storage and avoid exposing it in prompts, logs, committed files, or persisted outputs. <br>
Risk: Persisted product-query responses may contain pricing, user-supplied search text, or other sensitive business data. <br>
Mitigation: Write response files outside git working trees, extract only needed fields, and delete persisted files when the task is complete. <br>
Risk: Feedback submissions may include confidential user text if the agent sends raw task details. <br>
Mitigation: Avoid sending confidential user text as feedback; summarize only non-sensitive intent, result, and issue details. <br>


## Reference(s): <br>
- [EHunt Temu Product Query API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-ehunt-temu-product-query) <br>
- [LinkFox Tool Gateway Endpoint](https://tool-gateway.linkfox.com/ehunt/temu/productQuery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and optional shell commands; direct script calls return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Large responses may be persisted to local JSON files for later field extraction; persisted files are not automatically deleted.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
