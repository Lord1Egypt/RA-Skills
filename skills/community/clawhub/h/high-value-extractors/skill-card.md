## Description: <br>
Extract structured data from product pages, job listings, and company pages. Plus generate working AI endpoints from schemas. LLM-powered extraction micro-services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renoblabs](https://clawhub.ai/user/renoblabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract structured product, job, and company data from web pages, or to generate FastAPI endpoint code from supplied schemas. Calls use paid x402 endpoints with disclosed USDC pricing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each endpoint call can spend USDC. <br>
Mitigation: Use payment controls and review pricing before allowing an agent to call the paid x402 endpoints. <br>
Risk: Submitted URLs may expose private, internal, or personal-data-heavy pages to the service operator. <br>
Mitigation: Only submit URLs the user is authorized to process and where the service operator is trusted. <br>
Risk: Generated FastAPI code may be unsafe or unsuitable to deploy as-is. <br>
Mitigation: Review and test generated code before running or deploying it. <br>


## Reference(s): <br>
- [High-Value Extractors on ClawHub](https://clawhub.ai/renoblabs/high-value-extractors) <br>
- [renoblabs publisher profile](https://clawhub.ai/user/renoblabs) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples, plus generated FastAPI code where applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 calls disclose $0.02 USDC extraction pricing and $0.10 USDC endpoint-generation pricing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
