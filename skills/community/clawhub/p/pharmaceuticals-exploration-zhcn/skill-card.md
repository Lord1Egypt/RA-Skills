## Description: <br>
Guides Chinese-language pharmaceutical research by using PatSnap Life Science MCP data to summarize drug identity, mechanisms, safety, clinical status, competitive landscape, and drug deal evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Life science analysts, pharmaceutical researchers, and business development teams use this skill to investigate named drugs, diseases, targets, clinical trials, safety signals, competitive positioning, and drug transaction records. The skill is intended for Chinese-language research workflows that can connect to the required PatSnap Life Science MCP services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PatSnap API key and sends pharmaceutical research queries to external PatSnap services, and sometimes to web search providers when MCP data is insufficient or current information is requested. <br>
Mitigation: Use a dedicated or revocable API key, verify the PatSnap endpoint before connecting, and avoid submitting confidential research questions unless the provider's data handling is acceptable. <br>
Risk: Pharmaceutical, safety, clinical, and competitive analyses can be incomplete or misleading if source databases are stale, unavailable, or insufficient for the user's question. <br>
Mitigation: Treat outputs as research support, verify key claims against primary clinical, regulatory, patent, literature, and transaction records, and require expert review before medical, investment, or regulatory decisions. <br>
Risk: Setup commands place an API key in an MCP connection URL, which can expose credentials through shell history, logs, screenshots, or shared configuration. <br>
Mitigation: Use scoped credentials where available, avoid sharing command output or configuration containing keys, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [PatSnap Open Platform](https://open.patsnap.com) <br>
- [Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [Chemical Molecular MCP Server](https://open.patsnap.com/marketplace/mcp-servers/713886) <br>
- [Biology Modality MCP Server](https://open.patsnap.com/marketplace/mcp-servers/06e741) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Developer Documentation](https://open.patsnap.com/devportal) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown reports with Chinese headings, tables when useful, citation summaries, and inline shell setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured Chinese pharmaceutical research guidance that depends on successful PatSnap MCP connectivity and may supplement MCP data with web search only when the skill's criteria are met.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
