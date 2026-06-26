## Description: <br>
GTmetrix reads, creates, and updates GTmetrix data through the OOMOL gtmetrix connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate GTmetrix through an OOMOL-connected account, including reading account status, pages, reports, tests, browsers, locations, and simulated devices. It can also start new GTmetrix performance tests after confirming the payload and effect with the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires use of OOMOL as an intermediary for the connected GTmetrix account. <br>
Mitigation: Install and use it only when that account-routing model is acceptable for the user or organization. <br>
Risk: The start_test action can spend GTmetrix credits or create new account activity. <br>
Mitigation: Review the exact payload and obtain user confirmation before running start_test. <br>


## Reference(s): <br>
- [GTmetrix homepage](https://gtmetrix.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-gtmetrix) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to inspect GTmetrix action schemas and run connector actions; command responses include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
