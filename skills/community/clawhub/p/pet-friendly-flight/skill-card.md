## Description: <br>
Search for pet-friendly flights with animal cabin and pet carrier options, and support related travel booking tasks through Fliggy-powered flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to collect route details, run flyai flight searches, and present pet-friendly flight options with booking links. It is also framed for adjacent travel booking tasks such as hotels, trains, attraction tickets, insurance, and car rental when supported by the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may globally install and run an unpinned third-party flyai CLI package without an explicit consent gate. <br>
Mitigation: Preinstall or approve a known FlyAI CLI version before use, and require user approval before any global package installation. <br>
Risk: Flight availability, prices, and pet cabin or carrier policies may be incomplete or change before booking. <br>
Mitigation: Use CLI output only as a booking lead and verify pet travel rules directly with the airline before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/pet-friendly-flight) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, pet travel tips, and inline bash commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include Book links from detailUrl values, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
