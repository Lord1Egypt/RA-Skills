## Description: <br>
Query `.ics` calendar files, raw iCal strings, or remote iCal feeds with the local `icali` CLI. Use when a user asks for natural-language calendar lookups such as what's on a day, week, or time window, whether a person appears in upcoming meetings, or when filtering iCal events by summary, description, location, date range, status, or component type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[docmarionum1](https://clawhub.ai/user/docmarionum1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language calendar questions into focused `icali` queries against provided iCal sources. It helps answer schedule, date-window, participant, status, and keyword-filter questions with concise calendar summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read calendar contents from local `.ics` files, raw iCal text, or remote feed URLs provided to the agent. <br>
Mitigation: Use only calendar files and feed URLs that the user is authorized to share, and avoid private feed URLs unless their contents are intended to be queried and summarized. <br>
Risk: The skill depends on the local `icali` CLI, so an untrusted or unexpected binary on the PATH could affect behavior. <br>
Mitigation: Install `icali` from a trusted source and verify the binary location before enabling the skill in sensitive environments. <br>
Risk: Ambiguous timezone or date-window interpretation can produce misleading calendar answers. <br>
Mitigation: Provide an IANA timezone when local day boundaries matter and have the agent state the interpreted date or datetime window in its answer. <br>


## Reference(s): <br>
- [iCaLI project homepage](https://github.com/docmarionum1/iCaLI) <br>
- [ClawHub skill page](https://clawhub.ai/docmarionum1/ical-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and natural-language calendar summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize JSON returned by `icali`; requires a user-provided or discoverable iCal file, raw iCal string, or remote feed URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
