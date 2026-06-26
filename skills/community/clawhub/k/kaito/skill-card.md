## Description: <br>
Kaito helps agents query Kaito mindshare data for crypto entities or narratives and summarize trends, rank context, historical range, and movement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YH9277](https://clawhub.ai/user/YH9277) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use Kaito to check mindshare trends for tokens, projects, and Kaito narrative IDs, either standalone with user confirmation or as part of social-listening, strategy, and investigation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Entity and narrative query details may be handled by the configured Kaito MCP provider. <br>
Mitigation: Avoid including private, secret, or sensitive information in entity or narrative prompts. <br>
Risk: Case mismatches or unsupported narrative IDs may return empty or misleading results. <br>
Mitigation: Use the documented case-sensitive narrative IDs and fall back to keyword search when an ID is not supported. <br>
Risk: Ticker-only lookups can produce all-zero data when Kaito indexes an entity by full project name. <br>
Mitigation: Retry all-zero ticker results with the full project name before presenting the trend. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YH9277/kaito) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text summary with optional structured data for workflow skills] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Standalone use confirms parameters first; workflow use accepts passed parameters directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
