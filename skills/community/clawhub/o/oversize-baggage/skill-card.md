## Description: <br>
Search for flights accommodating oversize baggage and sports equipment, with additional travel booking support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search live flight options for oversized baggage, sports equipment, and related travel bookings. It guides agents to collect route details, run the flyai CLI, and return Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install an unpinned global third-party CLI package before use. <br>
Mitigation: Review and install @fly-ai/flyai-cli manually from a trusted package source, pin or record the approved version, and verify `flyai --version` before allowing agent execution. <br>
Risk: Travel search details may be sent to flyai or Fliggy services during CLI searches. <br>
Mitigation: Run searches only with user-approved route, date, budget, and preference parameters, and avoid submitting sensitive personal information unless required and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/oversize-baggage) <br>
- [Parameter Collection & Output Templates](artifact/references/templates.md) <br>
- [Scenario Playbooks](artifact/references/playbooks.md) <br>
- [Failure Recovery](artifact/references/fallbacks.md) <br>
- [Execution Runbook](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and summaries with inline booking links and shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include booking links when available, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
