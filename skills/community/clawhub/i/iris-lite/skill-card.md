## Description: <br>
Iris Lite scans the last 25 Gmail emails, ranks urgency, lists priorities, and drafts two quick replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees can use this skill to perform a quick Gmail inbox triage, identify higher-priority recent messages, and prepare a small number of draft replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires IMAP access to the configured Gmail inbox through a Gmail app password. <br>
Mitigation: Use a dedicated Gmail app password, store it only in the required environment variable, and revoke it when access is no longer needed. <br>
Risk: Recent email headers, short snippets, urgency scores, and draft reply text may be displayed locally during triage. <br>
Mitigation: Run the skill only in a trusted local environment and review displayed summaries and draft replies before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/iris-lite) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/occupythemilkyway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and Python code blocks; runtime terminal text with priority summaries and draft replies.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gmail address and app password environment variables; scans up to 25 recent inbox messages and drafts up to 2 replies.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
