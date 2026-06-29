## Description: <br>
Run an agent against five prompt-injection attacks and produce a local behavior report covering credential leaks, metric fabrication, premature halt, runaway spend, and log falsification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weldog](https://clawhub.ai/user/weldog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA teams use this skill to run a local self-diagnostic harness against an agent and review observed behavior across five prompt-injection scenarios. The report helps compare safety outcomes with task quality, but it is not a signed badge or third-party attestation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to clone and run an external harness locally. <br>
Mitigation: Review the repository before execution and run it with a test agent command in a controlled environment. <br>
Risk: A looping or tool-using agent could consume time or resources during the robustness test. <br>
Mitigation: Set a reasonable per-pass timeout and avoid connecting production credentials or high-impact tools. <br>
Risk: A local self-diagnostic report could be mistaken for a signed third-party attestation. <br>
Mitigation: Treat local results as internal QA evidence only; use the verified service when a signed badge is required. <br>


## Reference(s): <br>
- [ibuildbots harness repository](https://github.com/Weldog/ibuildbots) <br>
- [ibuildbots verified service](https://ibuildbots.dev) <br>
- [ClawHub skill page](https://clawhub.ai/weldog/ibuildbots-verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, json] <br>
**Output Format:** [Markdown instructions with shell commands and a JSON report example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and git; the external harness writes a local state.json report.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
