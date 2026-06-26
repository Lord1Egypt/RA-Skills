## Description: <br>
Generates structured U.S. stock holding analysis and trade guidance from text or screenshots using current market, macro, sector, social, insider-flow, technical, and risk-control signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and developers use this skill to turn U.S. equity holdings or ticker questions into structured portfolio analysis, risk checks, and trade-action guidance. It supports text input and portfolio screenshots, with a confirmation step when image extraction is incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores portfolio information locally at ~/.openclaw/memory/portfolio.json without clear opt-in, retention, or deletion controls. <br>
Mitigation: Install only if local portfolio retention is acceptable; remove account identifiers from screenshots and delete or block ~/.openclaw/memory/portfolio.json if holdings should not persist. <br>
Risk: Trade advice can be incorrect or misleading if market data, extracted holdings, or model reasoning is wrong. <br>
Mitigation: Independently verify all trade advice and confirm extracted portfolio data before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonxu/my-stock-analysis-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown with structured tables and concise trade-action guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use user-provided holdings text or screenshots and may store a portfolio snapshot locally at ~/.openclaw/memory/portfolio.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
