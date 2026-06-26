## Description: <br>
Generates PizzINT reports that summarize Pentagon Pizza Index signals, DOUGHCON levels, pizza shop activity, PolyPulse threats, prediction-market signals, and OSINT updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai157isme-lgtm](https://clawhub.ai/user/kai157isme-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to inspect PizzINT-related signals and produce concise OSINT-style status reports for users tracking geopolitical risk indicators. The reports are for situational awareness and should not be treated as authoritative military, political, financial, or safety advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PizzINT outputs are speculative OSINT indicators and may be mistaken for authoritative geopolitical, military, financial, or safety advice. <br>
Mitigation: Present reports as situational awareness only, preserve uncertainty language, and require independent verification before decisions or actions. <br>
Risk: The live PizzINT site is client-side rendered, so script-only fetching can miss or misread current data. <br>
Mitigation: Use browser-based capture for live readings and rely on the parser only after data has been captured or when validating already available data. <br>
Risk: Broad geopolitical prompts may activate the skill when a user did not intend to run a PizzINT report. <br>
Mitigation: Narrow activation to explicit PizzINT, pizza index, Pentagon Pizza, or equivalent monitoring requests. <br>


## Reference(s): <br>
- [PizzINT live site](https://pizzint.watch/) <br>
- [ClawHub release page](https://clawhub.ai/kai157isme-lgtm/pizzint-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, status labels, warnings, and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include logic checks for NEH thresholds, DOUGHCON levels, threat labels, and source contradictions when data is available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
