## Description: <br>
Query Korean school information, meal menus, and timetables from the official NEIS OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techkwon](https://clawhub.ai/user/techkwon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to look up Korean school codes, meal menus, and class timetables through a bundled CLI. Agents can request JSON output when the result will be consumed by another tool, script, or UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to the official NEIS API and can include NEIS_API_KEY in request URLs when the key is set. <br>
Mitigation: Install only when NEIS school, meal, or timetable lookup is needed, and set NEIS_API_KEY only in environments where that request-url exposure is acceptable. <br>


## Reference(s): <br>
- [NEIS API Notes](artifact/references/neis-api.md) <br>
- [Official NEIS OpenAPI Portal](https://open.neis.go.kr/portal/mainPage.do) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes ok, command, endpoint, query, count, and data fields.] <br>

## Skill Version(s): <br>
0.2.1 (source: release evidence and CLI version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
