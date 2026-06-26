## Description: <br>
Finds OpenTable restaurant options and produces reservation deep links for user-confirmed booking handoff without submitting reservations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikehe123](https://clawhub.ai/user/mikehe123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search OpenTable by location, date, time, party size, and cuisine, then return a concise restaurant list or booking deep link. The user completes any reservation directly in OpenTable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The troubleshooting guidance can change a global browser SSRF allowlist and restart the OpenClaw gateway. <br>
Mitigation: Require administrator review before running that command, and prefer explicit preconfiguration of OpenTable browser access. <br>
Risk: Restaurant booking intent could be mistaken for permission to complete a reservation. <br>
Mitigation: Keep the skill limited to OpenTable deep links and require the user to confirm any reservation in their own OpenTable session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikehe123/opentable-reservations) <br>
- [OpenTable](https://www.opentable.com/) <br>
- [README](artifact/README.md) <br>
- [Benchmark](artifact/BENCHMARK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON-producing helper commands and OpenTable URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns compact restaurant lists, error guidance, or reservation handoff links; the skill does not complete bookings.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
