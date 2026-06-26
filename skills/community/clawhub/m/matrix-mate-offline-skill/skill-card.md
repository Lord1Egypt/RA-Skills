## Description: <br>
Matrix Mate parses ITA Matrix itinerary links, audits fare rules, and produces traveler-safe summaries through a local MCP runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skylinehk](https://clawhub.ai/user/skylinehk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers, points enthusiasts, premium-cabin deal hunters, and travel agents use this skill to parse ITA Matrix itinerary links through a local Matrix Mate app, audit fare-rule caveats, and export traveler-safe or agent-facing trip summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP runtime can be pointed at a non-local Matrix Mate base URL if the operator enables the remote override. <br>
Mitigation: Keep the default loopback-only setting and enable MATRIX_MATE_ALLOW_REMOTE_BASE_URL only for a host the operator explicitly trusts. <br>
Risk: Matrix pages, itinerary text, or fare-rule bundles can contain adversarial or misleading content. <br>
Mitigation: Treat browser content and tool output as data, keep Matrix Mate as the parse source of truth, and avoid autonomous booking, payment, login, or CAPTCHA workflows. <br>
Risk: Very large pasted JSON or fare-rule bundles may increase latency or resource use because size limits are not yet documented as enforced. <br>
Mitigation: Avoid submitting very large manual payloads until explicit size limits are added. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/skylinehk/matrix-mate-offline-skill) <br>
- [README](README.md) <br>
- [Security & Trust Notes](SECURITY.md) <br>
- [Local Matrix Mate Surfaces](references/local-surfaces.md) <br>
- [Browser-Assisted ITA Matrix Search](references/browser-search.md) <br>
- [Safety Boundary](references/safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and MCP tool responses in structured JSON or text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Matrix Mate app and Node/npm MCP runtime; browser use is limited to read/search and link capture.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
