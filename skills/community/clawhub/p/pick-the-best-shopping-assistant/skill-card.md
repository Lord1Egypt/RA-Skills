## Description: <br>
Pick the Best - Personal shopping assistant for product search, price comparison, and recommendations powered by Pick the Best. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nepp-an](https://clawhub.ai/user/nepp-an) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to search for products, compare prices, find deals, and receive shopping recommendations across supported Pick the Best markets. <br>

### Deployment Geography for Use: <br>
Global use, with shopping results targeted to United Kingdom, Germany, Poland, and France markets. <br>

## Known Risks and Mitigations: <br>
Risk: Shopping searches are sent to Pick the Best. <br>
Mitigation: Avoid including sensitive personal information in shopping prompts. <br>
Risk: Product links may include affiliate tracking. <br>
Mitigation: Review the destination page and purchasing terms before buying. <br>
Risk: Prices and availability may vary by country or currency. <br>
Mitigation: Specify the target market and verify final price, availability, and seller details on the merchant page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nepp-an/pick-the-best-shopping-assistant) <br>
- [Pick the Best shopping MCP endpoint](https://pickthebest.com/gb/en/v1/shopping/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown shopping recommendations with product summaries, links, and optional JSON-RPC curl examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product prices, ratings, platform names, affiliate-tracked origin URLs, and refinement suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
