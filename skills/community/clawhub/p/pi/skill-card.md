## Description: <br>
Personal investigator and people lookup skill for deep background research on a person using public records, court documents, property records, social media, corporate filings, and web OSINT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tag-assistant](https://clawhub.ai/user/tag-assistant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users or analysts use this skill to compile an OSINT-style investigation report about a named person from public records, web search, court, property, business, social, and donation sources. It should be used only for lawful, non-harassing purposes with careful review of sensitive findings before sharing. <br>

### Deployment Geography for Use: <br>
Global, subject to local privacy, public-records, and permissible-use laws. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to mine private local contacts, payments, calls, messages, and memory while investigating a person. <br>
Mitigation: Disable or remove local-data searches unless the user gives explicit per-run consent and the purpose is lawful and non-harassing. <br>
Risk: The skill can collect sensitive personal details such as contact information, addresses, family connections, legal records, and financial indicators. <br>
Mitigation: Minimize sensitive details, avoid SSNs, driver's license numbers, and exact home or contact details, and review any generated dossier carefully before sharing. <br>
Risk: People-search aggregators and public records can conflate people with similar names. <br>
Mitigation: Verify findings against identity anchors, label uncertain claims clearly, and avoid attributing unverified information to the target person. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tag-assistant/pi) <br>
- [Court Systems Quick Reference](references/court-systems.md) <br>
- [People Search and OSINT Resources](references/osint-resources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown dossier with source links, caveats, and optional shell command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confidence notes, disambiguation notes, and leads requiring manual follow-up.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
