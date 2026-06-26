## Description: <br>
Query the SEC EDGAR database to find companies, retrieve recent filings by form type, and access key financial metrics from XBRL data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, finance teams, and developers use this skill to let an agent search public companies, retrieve SEC filing metadata by CIK and form type, and access recent XBRL financial facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, tickers, CIKs, form filters, and filing queries are sent to the disclosed Pipeworx gateway. <br>
Mitigation: Use the skill for public-company SEC research only, and avoid workflows where query privacy or third-party service provenance is a concern. <br>
Risk: Agents may treat returned filing summaries or financial facts as final analysis. <br>
Mitigation: Review the linked SEC filing documents and source values before making financial, legal, investment, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-sec) <br>
- [Pipeworx SEC MCP Gateway](https://gateway.pipeworx.io/sec/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and JSON-RPC examples; MCP tool responses return company identifiers, filing metadata, document links, and financial facts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to the disclosed Pipeworx SEC MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
