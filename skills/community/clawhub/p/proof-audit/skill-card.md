## Description: <br>
Run a Proof Audit on a company's website to find social proof such as testimonials, case studies, and reviews, score freshness on a five-band scale, and recommend what to refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[growthnation](https://clawhub.ai/user/growthnation) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators, marketers, and growth teams use this skill to audit a company's website for stale social proof and prioritise updates that improve buyer credibility. It can run from web search and fetch alone, with optional GrowthNation MCP assistance when the user's saved proof library is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes conclusions and refresh recommendations based on live website content and optional connected library data, so findings may be incomplete or misleading if pages are missed or evidence is stale. <br>
Mitigation: Review the quoted date evidence, capped-page note, and recommendations before using the audit for customer-facing decisions. <br>
Risk: The skill may suggest use of optional GrowthNation MCP tools when connected, which can access saved proof library data for the signed-in user. <br>
Mitigation: Use MCP-assisted mode only when the user is authenticated, on an eligible plan, and expects their saved proof library to be included; otherwise fall back to web-only mode. <br>


## Reference(s): <br>
- [ClawHub Proof Audit release page](https://clawhub.ai/growthnation/proof-audit) <br>
- [GrowthNation publisher profile](https://clawhub.ai/user/growthnation) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with per-page freshness table, coverage gaps, and prioritised recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Worst-first scoring table with quoted evidence for each freshness number; caps discovery at roughly 8-12 pages when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
