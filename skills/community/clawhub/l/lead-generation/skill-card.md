## Description: <br>
Lead Generation finds high-intent buyers in live Twitter, Instagram, and Reddit conversations, researches a product, generates targeted search queries, and discovers people actively looking for solutions the product offers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, growth, marketing, and customer discovery teams use this skill to identify prospects who are expressing buyer intent, competitor frustration, or active solution-seeking behavior on social platforms. The skill helps an agent research the product, generate search queries, score leads, and draft outreach for user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privacy exposure from product, customer, or lead data used in searches or stored in local lead-generation files. <br>
Mitigation: Avoid confidential product plans or sensitive customer data in generated queries, and periodically review or delete data/lead-generation files. <br>
Risk: Dependency and service trust risk from Xpoz, the OAuth setup flow, and the mcporter npm package. <br>
Mitigation: Install only if you trust Xpoz, the xpoz-setup OAuth flow, and the mcporter npm package. <br>
Risk: Outreach drafts could be inaccurate, misleading, or unsuitable to send as written. <br>
Mitigation: Manually review all outreach drafts before sending and disclose affiliations. <br>


## Reference(s): <br>
- [Xpoz](https://xpoz.ai) <br>
- [Lead Generation on ClawHub](https://clawhub.ai/atyachin/lead-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with lead summaries, scoring rationale, outreach drafts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON files under data/lead-generation for product profiles, generated queries, and sent-lead deduplication.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
