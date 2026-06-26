## Description: <br>
Generates realistic fake user profiles with names, contact details, addresses, nationalities, and profile photo URLs through the Pipeworx randomuser MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request fake user profile data for testing, placeholder content, and sample workflows that need realistic personal details without using real people. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to an external Pipeworx endpoint and generated profile-picture URLs may come from external services. <br>
Mitigation: Confirm that external network use is acceptable before installing or using the skill. <br>
Risk: Generated fake identity data could be misused for impersonation or fraud. <br>
Mitigation: Use generated profiles only for testing, placeholder content, and sample data workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-randomuser) <br>
- [Pipeworx randomuser MCP endpoint](https://gateway.pipeworx.io/randomuser/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces fake profile fields including name, email, username, UUID, date of birth, phone numbers, nationality, address, and profile picture URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
