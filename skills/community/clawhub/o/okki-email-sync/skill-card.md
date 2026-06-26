## Description: <br>
Synchronize email activities and quotation events with OKKI CRM as follow-up trail records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM automation maintainers use this skill to log sent emails and generated quotations into OKKI CRM follow-up trails while matching customers by domain lookup and vector search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy email body excerpts, quotation details, and attachment names into OKKI CRM and local state files. <br>
Mitigation: Confirm the allowed customer data scope before deployment and restrict syncing to approved workflows and accounts. <br>
Risk: The skill depends on configured OKKI CLI and vector-search script paths. <br>
Mitigation: Verify those paths before installation and run them with least-privilege access. <br>
Risk: Runtime state and unmatched-email logs are written under /tmp by default. <br>
Mitigation: Move or protect the state and log files before processing sensitive customer communications. <br>


## Reference(s): <br>
- [OKKI Email Sync ClawHub Release](https://clawhub.ai/cjboy007/okki-email-sync) <br>
- [Publisher Profile](https://clawhub.ai/user/cjboy007) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CRM sync guidance and integration code paths for OKKI email and quotation trail creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
