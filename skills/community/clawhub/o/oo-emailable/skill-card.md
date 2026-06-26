## Description: <br>
Emailable (emailable.com). Use this skill for ANY Emailable request, including searching and reading data, instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Emailable through an OOMOL-connected account, including checking account details, verifying individual email addresses, and managing batch verification jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch email verification creates remote Emailable jobs and may consume account credits. <br>
Mitigation: Require explicit confirmation of the exact email list and expected credit or billing impact before running verify_batch_emails. <br>
Risk: The skill uses a connected Emailable account through OOMOL and therefore depends on sensitive account credentials managed outside the agent. <br>
Mitigation: Install only when the user is comfortable allowing agent actions through the connected Emailable account, and run setup or reconnection steps only after an authentication or connection failure. <br>


## Reference(s): <br>
- [Emailable homepage](https://emailable.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-emailable) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include JSON data and an execution id under meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
