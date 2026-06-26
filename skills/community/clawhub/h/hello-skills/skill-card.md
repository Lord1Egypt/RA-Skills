## Description: <br>
hello-skills returns a greeting-style execution response using supplied name, symbol, timeframe, and message parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuwenquant](https://clawhub.ai/user/fuwenquant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents can use this release as a lightweight parameter echo skill to confirm invocation flow and return a structured status, message, and data payload. It should not be used for real trading analysis or signal generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release description suggests quantitative strategy analysis and signal generation, but the artifact only returns a greeting-style response with echoed parameters. <br>
Mitigation: Treat outputs as status and echo data only; do not use them for trading decisions or signal generation. <br>


## Reference(s): <br>
- [ClawHub page for hello-skills](https://clawhub.ai/fuwenquant/hello-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON-compatible data] <br>
**Output Format:** [JSON-compatible object with status, message, and data fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success, message, and data fields; data includes name, symbol, timeframe, message, and a fixed timestamp.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
