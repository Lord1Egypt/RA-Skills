## Description: <br>
Cnc Quick Probe helps agents collect missing CNC quote parameters including material, quantity, tolerance, surface finish, and Ra before handing off to quoting when enough information is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill during CNC quote intake to ask for missing manufacturing parameters before generating or handing off a quote. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically route to a CNC quote system once it judges that enough parameters have been collected. <br>
Mitigation: Review generated quotes before relying on them or sending them to customers. <br>
Risk: The skill depends on a local cnc-quote-system workspace dependency. <br>
Mitigation: Install only when the referenced local quote system is expected and trusted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted parameter questions and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Collects up to five CNC manufacturing parameters and reports whether the quote is ready.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
