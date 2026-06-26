## Description: <br>
Creates one or many mailbox addresses in a Cloudflare temporary mail system through the /admin/new_address admin API and returns structured results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcwang502](https://clawhub.ai/user/jcwang502) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create single or batch mailbox addresses through a Cloudflare temporary mail system admin API, including JSON or CSV output for downstream handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create mailboxes using admin credentials. <br>
Mitigation: Use least-privilege admin credentials and confirm the target API URL, domain, and requested mailbox count before execution. <br>
Risk: Returned JWTs, passwords, and exported JSON or CSV files may contain secrets. <br>
Mitigation: Treat script output and output files as sensitive, avoid writing them to shared paths, and delete them when no longer needed. <br>
Risk: Batch creation can create many addresses in one run. <br>
Mitigation: Review batch inputs, de-duplicated names, and the destination domain before allowing the agent to run the command. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jcwang502/mail-addr-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [JSON or CSV from the helper script, with concise Markdown guidance when summarizing for a user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mailbox JWTs, passwords, and CSV or JSON output files that should be treated as secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
