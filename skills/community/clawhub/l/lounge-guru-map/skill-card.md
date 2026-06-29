## Description: <br>
Lounge Guru Map provides offline, air-gapped lookup, filtering, briefing, and comparison over a bundled airport lounge catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skylinehk](https://clawhub.ai/user/skylinehk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to answer airport lounge lookup, facility filtering, airport brief, and lounge comparison questions from a bundled offline snapshot when network access is unavailable or disallowed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled lounge catalog is an offline snapshot generated on 2026-03-11 and may be stale or incomplete for current lounge access, availability, or rules. <br>
Mitigation: State that answers are grounded in the offline snapshot and verify current lounge details through an official or live source when freshness matters. <br>
Risk: Users may ask for lounges or data that are outside the bundled snapshot. <br>
Mitigation: Report missing coverage or stale data explicitly instead of inferring newer information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skylinehk/lounge-guru-map) <br>
- [Offline MCP Setup](references/mcp.md) <br>
- [Offline Safety](references/safety.md) <br>
- [Offline Publishing Notes](references/publishing.md) <br>
- [Bundled catalog snapshot](assets/catalog.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local MCP tool results and JSON-structured catalog records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bounded local MCP queries over a bundled offline catalog; it does not provide live lounge availability or access rules.] <br>

## Skill Version(s): <br>
1.3.27 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
