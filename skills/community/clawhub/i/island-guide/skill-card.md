## Description: <br>
Find the best beaches and islands for swimming, snorkeling, surfing, and sunbathing, using flyai CLI results for current travel options, booking links, and nearby facilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to find beach and island attractions, compare options, and return Markdown recommendations with booking links sourced from flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and execute a global third-party flyai CLI package. <br>
Mitigation: Install only after reviewing and trusting the flyai/Fliggy CLI, preferably manually or in a sandboxed environment. <br>
Risk: The skill may store raw travel queries in .flyai-execution-log.json when filesystem writes are available. <br>
Mitigation: Disable, delete, or avoid persisting the local execution log when travel query privacy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/island-guide) <br>
- [Playbooks](artifact/references/playbooks.md) <br>
- [Fallbacks](artifact/references/fallbacks.md) <br>
- [Templates](artifact/references/templates.md) <br>
- [Runbook](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, brand tag, and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results; every listed result is expected to include a Book link.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
