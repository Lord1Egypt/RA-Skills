## Description: <br>
Helps agents search and present real-time flight options for offsite meetings and strategy retreats using flyai/Fliggy results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and travel coordinators use this skill to collect route, date, and cabin preferences, run flight searches, and present booking options for business offsites or strategy retreats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run an unpinned global third-party npm CLI. <br>
Mitigation: Review the package first, install a pinned version manually where possible, and require user approval before any global installation. <br>
Risk: Flight-search details may be sent to flyai/Fliggy during CLI execution. <br>
Mitigation: Use the skill only when sharing the requested travel details with that service is acceptable. <br>
Risk: The description mentions broader travel services while the artifact primarily defines flight-search workflows. <br>
Mitigation: Limit deployment expectations to flight search unless additional supported workflows are reviewed and validated. <br>


## Reference(s): <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/offsite-meeting) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown flight search summaries with comparison tables and booking links, plus shell commands when execution is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on CLI results and include booking links when flight results are returned.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
