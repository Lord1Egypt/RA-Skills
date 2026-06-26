## Description: <br>
Plan Golden Week (National Day) or Spring Festival trips by using flyai CLI data to find flights, hotels, train tickets, attractions, itinerary options, visa information, travel insurance, car rental, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to answer Golden Week, National Day, Spring Festival, and holiday travel requests with real-time flyai CLI results and booking links. It is intended for peak-season travel planning, price comparison, crowd avoidance, and fallback handling when live travel data is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on a global third-party npm CLI. <br>
Mitigation: Review the CLI package before installation and run it only in environments where global npm tools are allowed. <br>
Risk: Travel queries or command details may be stored locally through execution logging. <br>
Mitigation: Avoid passport, payment, and highly sensitive itinerary details unless logging is disabled, isolated, or redacted. <br>
Risk: The security evidence marks the release as suspicious because raw travel queries and command logs can persist without clear notice or retention controls. <br>
Mitigation: Use the skill only after reviewing the logging behavior and retention expectations for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/golden-week) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, concise guidance, and inline shell commands when setup or retry steps are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include booking links when results are shown, and avoid raw JSON.] <br>

## Skill Version(s): <br>
v3.2.3 (source: server release evidence; artifact frontmatter reports 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
